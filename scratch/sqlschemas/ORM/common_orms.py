import os
import uuid

#-------[  Import SQLAlchemy ]---------
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence

#-------[  Import From Other Modules   ]---------
from common_base import Base, engine




# =====================================================================
# >>>>>>>>>>>>>>>>>>[    Common ORMs     ] >>>>>>>>>>>>>>>>>>>>>>>>>>>>
# =====================================================================
"""
    Common tables can't be treated as resources,
    If do so, it'll cause Loop Import problems.
"""


class User(Base):
    """ [  Store User's Private Data  ]
    :primary keys: [uid, host_id, user_id]
    :field uid: Unique UserID in current database
    :field host_id:
    :field user_id: UserID on specific Host site
    """
    __tablename__ = 'u_Users'

    uid = Column('uid', String, primary_key=True)
    host_id = Column('host_id', Integer, ForeignKey('hosts.id'), primary_key=True)
    user_id = Column('user_id', String, primary_key=True)

    name = Column('name', String)
    external_urls = Column('external_urls', String)
    followers = Column('followers', Integer, default=0)
    href = Column('href', String)
    images = Column('images', String)
    user_type = Column('type', String)
    uri = Column('uri', String)

    @staticmethod
    def add(session, host_id, jsondata):
        user = User(
            uid = str(uuid.uuid1().hex),
            host_id = host_id,
            user_id = jsondata['id'],
            name = jsondata['display_name'],
            external_urls = jsondata['external_urls']['spotify'],
            followers = jsondata['followers']['total'],
            href = jsondata['href'],
            images = str(jsondata['images']),
            user_type = jsondata['type'],
            uri = jsondata['uri']
        )
        session.merge(user)
        session.commit()
        print('[  OK  ] Inserted User: {}.'.format( user.name ))

        return user


class Host(Base):
    """ [ Music Information Host Providers ]
    :PK name:
    :KEY host_type: [MediaProvider, InfoProvider, FileSystem]
    :KEY uri: API entry point.
    :KEY tbname_*: Related table names in database
    :Note :
        Host class is an 'origin' class & can't be treated as a resource
        If not so, it'll cause Loop Import problem.
    """
    __tablename__ = 'hosts'

    id = Column('id', String, primary_key=True)
    name = Column('name', String)

    host_type = Column('type', String)
    uri = Column('URI', String)
    info = Column('info', String)

    tbname_track = Column('tbname_track', String)
    tbname_album = Column('tbname_album', String)
    tbname_artist = Column('tbname_artist', String)
    tbname_playlist = Column('tbname_playlist', String)

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
        j = jsondata
        item = cls(
            id = j['id'],
            name=j['name'],
            host_type=j['type'],
            uri=j['uri'],
            info=j['info'],
            tbname_track=j['tbname_track'],
            tbname_album=j['tbname_album'],
            tbname_artist=j['tbname_artist'],
            tbname_playlist=j['tbname_playlist']
        )
        session.merge( item )   #Merge existing data
        #session.commit()  #-> Better to commit after multiple inserts

        return item




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
            ref_id=str(uuid.uuid1().hex),
            src_id=src_id,
            host_id=host_id
        )
        session.merge(ref)
        #session.commit()  #-> Better to commit after multiple inserts
        return ref






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
            uitem = cls.add(session, uid, ref.ref_id, data)

            user_items.append( uitem )

        session.commit()
        print('[  OK  ] Inserted {} User {}s.'.format(
            len(user_items), cls.src_type
        ))
        return user_items

    @classmethod
    def add(cls, session, host_id, uid, jsondata):
        """ [ add single item ]
        :param {jsondata} single JSON object type:
        """
        print( 'Abstract class method to be implemented.' )






# ==============================================================
# >>>>>>>>>>>>>>>>>>>[    METHODS     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


def main():
    #------- Start of Data Submitting ---------

    # Clearout all existing tables
    try:
        User.__table__.drop(engine)
    except Exception as e:
        print('Error on dropping User table.')

    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)

    # Declare a common session for multiple files
    session = sessionmaker(bind=engine, autoflush=False)()


    # Start of Data Insersions --------{
    import os, json
    cwd = os.path.split(os.path.realpath(__file__))[0]
    # Add Hosts
    with open('{}/hosts.json'.format(os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )
    hosts = Host.add_sources(session, data['hosts'])
    # Add a User
    h1 = session.query(Host).first()
    with open('{}/spotify/jsondumps-full/get_user_profile.json'.format(os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )

    User.add(session, h1.id, data)
    # }------- End of Data Insersions

    session.commit()
    session.close()
    #------- End of Data Submitting ---------



if __name__ == '__main__':
    main()



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
