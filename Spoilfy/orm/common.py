#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:
#   - $ pip install sqlalchemy
#   - /tmp/db_spoilfy_uri.sqlite

import uuid

# -------[  Import SQLAlchemy ]---------
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Float


# Declare a common base for multiple files
Base = declarative_base()

# Connect Database
engine = create_engine('sqlite:////tmp/db_spoilfy_uri.sqlite', echo=False)

# Session
session = sessionmaker(bind=engine, autoflush=False)()


# ==============================================================
# >>>>>>>>>>>>>>>>>>[    Abstract ORMs     ] >>>>>>>>>>>>>>>>>>>
# ==============================================================

# For the use of decorator: @classproperty
class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


class SpoilfyORM(Base):
    """ [ Abstract ORM class ]
    """
    __abstract__ = True

    @classproperty
    def query(cls):
        return session.query(cls)


class Resource(SpoilfyORM):
    """ [ Abstract ORM class ]
        Independent table, without any setup to relate User tables
        Manually search by id if needed.
    """
    __abstract__ = True

    # PKs
    uri = Column('uri', String, primary_key=True)
    name = Column('name', String)

    # ->
    full = Column('full', Boolean, default=True)

    # -> These 3 fields are included in URI
    id = Column('id', String)
    type = Column('type', String)
    provider = Column('provider', String, default='NONE')
    # ^ default value only work in DB
    # ^ but you can't get it within the program
    # ^ so you have to explicitly give value to it

    @classmethod
    def get(cls, uri):
        return session.query(cls).filter(cls.uri == uri).first()

    def __new__(cls, *args, **kwargs):
        # print( '[  OK  ]__new__ {}'.format(cls) )
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = session.query(self.__class__)

    def __repr__(self):
        # return '<{} "{}">'.format( self.__class__.__name__, self.uri )
        return '<ORM [{}] at {}>'.format(self.name, self.uri)

    def __hash__(self):
        return hash((self.uri))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.uri == other.uri


# ==============================================================
# >>>>>>>>>>>>>>>>[    COMMON ORMs     ] >>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


class Reference(SpoilfyORM):
    """ [ References to map resources from different providers ]
        It maps things with SAME type but at different places.
    :PK uri: refer to the target resource.
    :KEY real_uri: as the REAL EXISTENCE of a resource.
    """
    __tablename__ = 'references'

    # PKs
    uri = Column('uri', String, primary_key=True)
    real_uri = Column('real_uri', String)

    nlinked = Column('nlinked', Integer, default=1)
    confidence = Column('confidence', Float, default=0)

    type = Column('type', String)
    provider = Column('provider', String)
    # ^ default value only take effect after inserted to DB

    @classmethod
    def get(cls, uri):
        return session.query(cls).filter(cls.uri == uri).first()

    def __init__(self, item, real_uri=None, confidence=1):
        super().__init__(
            uri=item.uri,
            real_uri=real_uri if real_uri else 'app:{}:{}'.format(
                item.type, str(uuid.uuid1().hex)
            ),
            type=item.type,
            provider=item.provider,
            confidence=confidence,
        )

    def __repr__(self):
        return '<REF "{}">'.format(self.real_uri)


class Include(SpoilfyORM):
    """ [ A Middleware for Many-to-Many relationship ]

        It maps:
        - Artist(s) include -> Album(s)
        - Album(s)  include -> Track(s)
    """

    __tablename__ = 'includes'

    # PKs/FKs
    parent_uri = Column('parent_uri', String, primary_key=True)
    child_uri = Column('child_uri', String, primary_key=True)

    parent_type = Column('parent_type', String)
    child_type = Column('child_type', String)
    provider = Column('provider', String)

    @classmethod
    def get(cls, uri):
        return session.query(cls).filter(cls.uri == uri).first()

    def __repr__(self):
        return '<{} INCLUDE "{}">'.format(self.parent_uri, self.child_uri)

    def __init__(self, p_uri, c_uri):
        super().__init__(
            parent_uri=p_uri,
            child_uri=c_uri,
            parent_type=p_uri.split(':')[-2],
            child_type=c_uri.split(':')[-2],
            provider=c_uri.split(':')[0],
        )


class UnTagged(SpoilfyORM):
    """ [ Store items miss tagged or can't be tagged ]
    """
    __tablename__ = '_untagged'

    real_uri = Column('real_uri', String, primary_key=True)

    def __init__(self, real_uri):
        super().__init__(
            real_uri=real_uri
        )


class Incomplete(SpoilfyORM):
    """ [ Store 'incomplete' items ]
    """
    __tablename__ = '_incompletes'

    real_uri = Column('real_uri', String, primary_key=True)

    def __init__(self, real_uri):
        super().__init__(
            real_uri=real_uri
        )


# ==============================================================
# >>>>>>>>>>>>>>>>>>[    TEST RUN     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


if __name__ == '__main__':
    try:
        # Reference.__table__.drop(engine)
        # Include.__table__.drop(engine)
        # UnTagged.__table__.drop(engine)
        # Incomplete.__table__.drop(engine)
        pass
    except Exception as e:
        print('Error on dropping User table.')
    finally:
        Base.metadata.create_all(bind=engine)


print('[  OK  ] __IMPORTED__: {}'.format(__name__))
