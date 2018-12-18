import uuid

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence


#-------[  Import From Other Modules   ]---------
from common_base import Base, engine, session
from CREATE_HOSTS import Host
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

    #def __init__(self, uid, src):
    #    self.uid = uid

    def addSource(self, src):
        """
            1. Check if source EXISTS in Track Reference Table
            2. If exists, get the "tid",
            3. If not, Insert new data to TrackRef, and get the "tid".
        """
        pass



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
        # }------- End of Data Insersions

    session.commit()
    session.close()
    #------- End of Data Submitting ---------



if __name__ == '__main__':
    main()



print('[  OK  ] IMPORTED: {}'.format(__name__))
