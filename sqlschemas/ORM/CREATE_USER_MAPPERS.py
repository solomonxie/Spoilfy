import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence

#-------[  Import From Other Modules   ]---------
from common_base import Base, engine
from CREATE_HOSTS import Host
from CREATE_USERS import User
from CREATE_TRACKS import TrackRef, Track_SPT, Track_MBZ



# =====================================================================
# >>>>>>>>>>>>>>>>>>[    User Tables     ] >>>>>>>>>>>>>>>>>>>>>>>>>>>>
# =====================================================================


class UserHost(Base):
    """[  User's favorite tracks  ]
    :PK [host_id, uid]: Composite primary keys
    """
    __tablename__ = 'u_Hosts'

    uid = Column('uid', String,
        ForeignKey('u_Users.uid'), primary_key=True
    )
    host_id = Column('host_id', String,
        ForeignKey('hosts.id'), primary_key=True
    )
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





class UserTrack(Base):
    """[  User's favorite tracks  ]
    :PK [ref_id, uid]: Composite primary keys
    :staticmethod add_from_spotify: 
    """
    __tablename__ = 'u_Tracks'

    ref_id = Column('ref_id', String,
        ForeignKey('ref_Tracks.ref_id'), primary_key=True
    )
    uid = Column('uid', String,
        ForeignKey('u_Users.uid'), primary_key=True
    )
    last_played = Column('last_played', Date)
    added_at = Column('added_at', Date)
    count = Column('count', Integer)
    rate = Column('rate', Integer)
    memo = Column('memo', String)

    @staticmethod
    def add_from_spotify(session, uid, jsondata):
        # Add tracks to database
        tracks = Track_SPT.add_sources(session, jsondata)
        # Add track references
        refs = TrackRef.add_references(session, uid, tracks)
        # Add User Tracks
        user_tracks = []
        for ref in refs:
            ut = UserTrack(
                uid = uid,
                ref_id = ref.ref_id,
                last_played = None,
                added_at = None,
                count = 0,
                rate = 0,
                memo = ''
            )
            session.merge(ut)
            user_tracks.append(ut)

        session.commit()
        print( '[  OK  ] Inserted {} User Tracks.'.format(len(user_tracks)) )
        return user_tracks





# ==============================================================
# >>>>>>>>>>>>>>>>>>>[    METHODS     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================




# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


def main():
    #------- Start of Data Submitting ---------

    # Clearout all existing tables
    UserTrack.__table__.drop(engine)
    UserHost.__table__.drop(engine)

    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)

    # Declare a common session for multiple files
    session = sessionmaker(bind=engine, autoflush=False)()


    # Start of Data Insersions --------{
    import os, json
    cwd = os.path.split(os.path.realpath(__file__))[0]
    with open('{}/spotify/jsondumps-full/get_user_tracks.json'.format(os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )

    # Get a user
    user = session.query(User).first()
    # Get a host
    host = session.query(Host).first()
    # Add User Hosts
    UserHost.add(session, user.uid, host.id)
    # Add User Tracks
    UserTrack.add_from_spotify(session, user.uid, data)
    # }------- End of Data Insersions

    session.commit()
    session.close()
    #------- End of Data Submitting ---------



if __name__ == '__main__':
    main()



print('[  OK  ] IMPORTED: {}'.format(__name__))
