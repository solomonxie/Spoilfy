import uuid

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence


#-------[  Import From Other Modules   ]---------
from common_base import Base, engine, session
from CREATE_HOSTS import Host
from CREATE_USERS import User
from CREATE_TRACKS import TrackRef, TrackSource, Track_SPT, Track_MBZ



# =====================================================================
# >>>>>>>>>>>>>>>>>>[    User Tables     ] >>>>>>>>>>>>>>>>>>>>>>>>>>>>
# =====================================================================


class UserHost(Base):
    __tablename__ = 'u_Hosts'

    id = Column('id', Integer, primary_key=True)
    uid = Column('uid', Integer, ForeignKey('u_Users.uid'))
    host_id = Column('host_id', Integer, ForeignKey('hosts.id'))
    uid_on_host = Column('uid_on_host', Integer)
    auth = Column('auth', String)
    name = Column('name', String)
    nickname = Column('nickname', String)
    email = Column('email', String)
    info = Column('info', String)


class UserTrack(Base):
    __tablename__ = 'u_Tracks'

    id = Column('id', Integer, primary_key=True)
    uid = Column('uid', String, ForeignKey('u_Users.uid'))
    ref_id = Column('ref_id', String, ForeignKey('ref_Tracks.ref_id'))
    last_played = Column('last_played', Date)
    added_at = Column('added_at', Date)
    count = Column('count', Integer)
    rate = Column('rate', Integer)
    memo = Column('memo', String)

    @staticmethod
    def add_user_spotify_tracks(session, uid, jsondata):
        # Add tracks to database
        tracks = Track_SPT.add_tracks(session, jsondata)
        # Add track references
        refs = TrackRef.add_track_reference(session, tracks, uid)
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
    Base.metadata.drop_all(engine)

    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)


    # Start of Data Insersions --------{
    import os, json
    cwd = os.path.split(os.path.realpath(__file__))[0]
    with open('{}/spotify/jsondumps-full/get_user_tracks.json'.format(os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )

    # Get user
    user = session.query(User).first()

    tracks = UserTrack.add_user_spotify_tracks(session, user.uid, data)
    # }------- End of Data Insersions

    session.commit()
    session.close()
    #------- End of Data Submitting ---------



if __name__ == '__main__':
    main()



print('[  OK  ] IMPORTED: {}'.format(__name__))
