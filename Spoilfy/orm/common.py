#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:
#   - $ pip install sqlalchemy
#   - /tmp/db_spoilfy_uri.sqlite

import uuid

#-------[  Import SQLAlchemy ]---------
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

class SpoilfyORM(Base):
    """ [ Abstract ORM class ]
    """
    __abstract__ = True

    # Decorator: @classproperty
    class classproperty(object):
        def __init__(self, getter):
            self.getter= getter
        def __get__(self, instance, owner):
            return self.getter(owner)

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

    #-> These 3 fields are included in URI
    id = Column('id', String)
    type = Column('type', String)
    provider = Column('provider', String, default='NONE')
    # ^ default value only work in DB
    # ^ but you can't get it within the program
    # ^ so you have to explicitly give value to it

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.query = session.query(self.__class__)

    @classmethod
    def add_resources(cls, items):
        """[ Add Resources ]
        :param session: sqlalchemy SESSION binded to DB.
        :param LIST items: must be iteratable.
        :return: inserted resource objects.
        """
        all = [ cls(o) for o in items ]
        updates = [ session.merge( a ) for a in all ]
        session.commit()
        print('[  OK  ] Inserted {} items to [{}].'.format(
            len(all), cls.__tablename__
        ))
        return all


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
    #^ default value only take effect after inserted to DB

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


    @classmethod
    def add_resources(cls, items):
        all = [ session.merge( cls(o) ) for o in items ]
        session.commit()
        print('[  OK  ] Inserted {} new references.'.format( len(all) ))
        return all




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

    def __init__(self, p_uri, c_uri):
        super().__init__(
            parent_uri = p_uri,
            child_uri = c_uri,
            parent_type = p_uri.split(':')[1],
            child_type = c_uri.split(':')[1],
        )
        session.merge( self )
        # session.commit()



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
