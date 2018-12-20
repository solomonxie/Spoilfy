import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence

#-------[  Import From Other Modules   ]---------
from common_base import Base, engine
from common_orms import UserItem
from CREATE_HOSTS import Host
from CREATE_USERS import User
from CREATE_TRACKS import Track_SPT, Track_MBZ, Track_FS
from CREATE_ALBUMS import Album_SPT, Album_MBZ, Album_FS
from CREATE_ARTISTS import Artist_SPT, Artist_MBZ, Artist_FS



# =====================================================================
# >>>>>>>>>>>>>>>>>>[    User Tables     ] >>>>>>>>>>>>>>>>>>>>>>>>>>>>
# =====================================================================


class UserHost(Base):
    """[  User's favorite tracks  ]
    :PK [host_id, uid]: Composite primary keys
    """
    __tablename__ = 'u_Hosts'

    uid = Column('uid', String, ForeignKey('u_Users.uid'), primary_key=True)
    host_id = Column('host_id', String, ForeignKey('hosts.id'), primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('u_Users.user_id'))

    auth = Column('auth', String)
    name = Column('name', String)
    nickname = Column('nickname', String)
    email = Column('email', String)
    info = Column('info', String)

    @staticmethod
    def add(session, uid, host_id):
        user_host = UserHost(
            uid = uid,
            host_id = host_id
        )
        session.merge(user_host)
        session.commit()
        print( '[  OK  ] Inserted User Host: {}.'.format( host_id ) )

        return user_host





class UserTrack(UserItem):
    """[  User's favorite tracks  ]
    :PKs: [ref_id, uid]
    :field last_played: Last time played the track
    :field added_at: Time added to the source library
    :field rate: Personal rating to the track
    :field memo: Personal comments
    :staticmethod add_from_spotify: 
    """
    __tablename__ = 'u_Tracks'
    src_type = 'track'

    uid = Column('uid', String, ForeignKey('u_Users.uid'), primary_key=True)
    ref_id = Column('ref_id', String, ForeignKey('references.ref_id'), primary_key=True)

    last_played = Column('last_played', String)
    added_at = Column('added_at', String)
    count = Column('count', Integer)
    rate = Column('rate', Integer)
    memo = Column('memo', String)

    @classmethod
    def add(cls, session, uid, ref_id, jsondata):
        item = cls(
            uid = uid,
            ref_id = ref_id,
            last_played = None,
            added_at = jsondata['added_at'],
            count = 0,
            rate = 0,
            memo = ''
        )
        session.merge( item )
        #session.commit()  #-> Better to commit after multiple inserts



class UserAlbum(UserItem):
    """ [  User's saved albums  ]
    :PKs: [ref_id, uid]
    :field last_played: Last time played the album
    :field added_at: Time added to the source library
    :field rate: Personal rating to the album
    :field memo: Personal comments
    :staticmethod :
    """
    __tablename__ = 'u_Albums'
    src_type = 'album'

    uid = Column('uid', String, ForeignKey('u_Users.uid'), primary_key=True)
    ref_id = Column('ref_id', String, ForeignKey('references.ref_id'), primary_key=True)

    added_at = Column('added_at', String)
    count = Column('count', Integer)
    rate = Column('rate', Integer)
    memo = Column('memo', String)

    @classmethod
    def add(cls, session, uid, ref_id, jsondata):
        item = cls(
            uid = uid,
            ref_id = ref_id,
            added_at = jsondata['added_at'],
            count = 0,
            rate = 0,
            memo = ''
        )
        session.merge( item )
        #session.commit()  #-> Better to commit after multiple inserts



class UserArtist(UserItem):
    """ [  User's followed artists ]
    :PKs: [ref_id, uid]
    :field rate: Personal rating to the album
    :field memo: Personal comments
    :staticmethod :
    """
    __tablename__ = 'u_Artists'
    src_type = 'artist'


    uid = Column('uid', String, ForeignKey('u_Users.uid'), primary_key=True)
    ref_id = Column('ref_id', String, ForeignKey('references.ref_id'), primary_key=True)

    memo = Column('memo', String)

    @classmethod
    def add(cls, session, uid, ref_id, jsondata):
        item = cls(
            uid = uid,
            ref_id = ref_id,
            memo = ''
        )
        session.merge( item )
        #session.commit()  #-> Better to commit after multiple inserts




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
        UserHost.__table__.drop(engine)
        UserTrack.__table__.drop(engine)
        UserAlbum.__table__.drop(engine)
        UserArtist.__table__.drop(engine)
    except Exception as e:
        print('Error on dropping User Tables.')


    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)

    # Declare a common session for multiple files
    session = sessionmaker(bind=engine, autoflush=False)()


    # Start of Data Insersions --------{
    import os, json
    cwd = os.path.split(os.path.realpath(__file__))[0]

    # Get a user
    user = session.query(User).first()
    # Get a host
    host = session.query(Host).first()
    # Add User Hosts
    UserHost.add(session, user.uid, host.id)
    # Add User Tracks
    with open('{}/spotify/jsondumps-full/get_user_tracks.json'.format(
        os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )
        #UserTrack.add_from_spotify(session, host.id, user.uid, data)
        UserTrack.add_items(
            session, host.id, user.uid,
            data['items'], Track_SPT
        )
    # Add User Albums
    with open('{}/spotify/jsondumps-full/get_user_albums.json'.format(
        os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )
        #UserAlbum.add_from_spotify(session, host.id, user.uid, data)
        UserAlbum.add_items(
            session, host.id, user.uid,
            data['items'], Album_SPT
        )
    # Add User Artists
    with open('{}/spotify/jsondumps-full/get_user_artists.json'.format(
        os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )
        #UserArtist.add_from_spotify(session, host.id, user.uid, data)
        UserArtist.add_items(
            session, host.id, user.uid,
            data['artists']['items'], Artist_SPT
        )
    # }------- End of Data Insersions

    session.commit()
    session.close()
    #------- End of Data Submitting ---------



if __name__ == '__main__':
    main()



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
