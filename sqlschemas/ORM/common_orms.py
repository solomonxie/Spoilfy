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

class Resource(Base):
    """ [ Abstract ORM class ]
        Independent table, without any setup to relate User tables
        Manually search by id if needed.
    """
    __abstract__ = True

    id = Column('id', String, primary_key=True)
    name = Column('name', String)
    src_type = None  #-> To be filled by children classes

    @classmethod
    def add_sources(cls, session, jsonItems):
        """[ Add Resources ]
        :param session: SQLAlchemy session object connected to DB
        :param String jsondump: JSON data in string format
        :return: Class instances of track resources
        """
        all_items = []
        for j in jsonItems:
            item = cls.add(session, j)
            all_items.append( item )

        session.commit()
        print('[  OK  ] Inserted {} items to [{}].'.format(
            len(all_items), cls.__tablename__
        ))

        return all_items

    @classmethod
    def add(cls, session, jsondata):
        pass


class Reference(Base):
    """ [ References to map sources from different providers ]
    :PK type: Resource type, track/album/artist/playlist.
    :PK,FK host_id: Host provider's ID, for current DB only.
    :PK,FK ref_id: ID for reference as agent, for current DB only.
    :PK,FK src_id: ReSource ID, generated from Providers.
    :PKs : [type, ref_id, src_id, host_id]
    """
    #__abstract__ = True
    __tablename__ = 'references'

    src_type = Column('src_type', String, primary_key=True)
    ref_id = Column('ref_id', String, nullable=False)  #>> unique reference ID
    src_id = Column('src_id', String, primary_key=True, nullable=False)  #>> dynamic | not speicify FK

    # Problem: Foreign Key in SQLAlchemy CANNOT be inherited
    # Solution: Declare same ForeignKey in subclass again
    # See: https://sqlalchemy-html.readthedocs.io/en/rel_1_0_6/orm/inheritance.html
    host_id = Column('host_id', Integer, ForeignKey('hosts.id'), primary_key=True)


    @classmethod
    def add_references(cls, session, src_type, host_id, sources):
        references = []
        for src in sources:
            ref = cls.add(session, src_type, host_id, src.id)
            references.append(ref)

        session.commit()
        print('[  OK  ] Inserted {} [{}] references.'.format(
            len(references), src_type
        ))

        return references
    
    @classmethod
    def add(cls, session, src_type, host_id, src_id):
        ref = cls(
            src_type=src_type,
            ref_id=str(uuid.uuid1()),
            src_id=src_id,
            host_id=host_id
        )
        session.merge(ref)
        #session.commit()  #-> Better to commit after multiple inserts
        return ref



class UserItem(Base):
    """ [ Abstract class for managing User resources ]
    :PKs: [ref_id, uid]
    :field memo: Personal comments
    """
    __abstract__ = True

    #-> To be filled by children classes
    src_type = None 
    uid = None
    ref_id = None

    @classmethod
    def add_items(cls, session, host_id, uid, jsondata, srcClass):
        """ [ add batch items ]
        :param {jsondata} List type:
        :param {srcClass} Resource class type:
        """
        user_items = []
        for data in jsondata:
            src = srcClass.add(session, data)
            ref = Reference.add(session, cls.src_type, host_id, src.id)
            item = cls.add(session, uid, ref.ref_id, data)
            user_items.append( item )

        session.commit()
        print('[  OK  ] Inserted {} User items.'.format(
            len(user_items)
        ))
        return user_items

    @classmethod
    def add(cls, session, host_id, uid, jsondata):
        """ [ add single item ]
        :param {jsondata} single JSON object type:
        """
        pass
