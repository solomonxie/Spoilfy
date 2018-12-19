import os
import uuid

#-------[  Import SQLAlchemy ]---------
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence

#-------[  Import From Other Modules   ]---------
from common_base import Base, engine
from CREATE_HOSTS import Host
from CREATE_USERS import User


# ==============================================================
# >>>>>>>>>>>>>>>>>>[    Abstract ORMs     ] >>>>>>>>>>>>>>>>>>>
# ==============================================================

class Source(Base):
    """
    Abstract ORM class.
        Independent table, without any setup to relate User tables
        Manually search by id if needed.
    """
    __abstract__ = True

    id = Column('id', String, primary_key=True)
    name = Column('name', String)

    @classmethod
    def add_sources(cls, session, jsondata):
        pass


class Reference(Base):
    """ [ References to map sources from different providers ]
    :primary keys: [ref_id, src_id, host_id]
    :field ref_id: Reference ID, generated for current DB only.
    :field src_id: Source ID, generated from Providers.
    :foreignKey host_id: Provider ID, generated for current DB only.
    """
    __abstract__ = True

    ref_id = Column('ref_id', String, nullable=False)  #>> unique reference ID
    src_id = Column('src_id', String, primary_key=True, nullable=False)  #>> dynamic | not speicify FK

    # Problem: Foreign Key in SQLAlchemy CANNOT be inherited
    # Solution: Declare same ForeignKey in subclass again
    # See: https://sqlalchemy-html.readthedocs.io/en/rel_1_0_6/orm/inheritance.html
    host_id = Column('host_id', Integer, ForeignKey('hosts.id'), primary_key=True)


    @classmethod
    def add_references(cls, session, host_id, sources):
        references = []
        for src in sources:
            ref = cls.add(session, host_id, src)
            references.append(ref)

        session.commit()
        print( '[  OK  ] Inserted {} references.'.format(len(references)) )

        return references
    
    @classmethod
    def add(cls, session, host_id, source):
        ref = cls(
            ref_id=str(uuid.uuid1()),
            src_id=source.id,
            host_id=host_id
        )
        session.merge(ref)
        #session.commit()
        return ref

