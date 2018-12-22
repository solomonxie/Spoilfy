import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence

#-------[  Import From Other Modules   ]---------
from common_base import Base, engine
from common_orms import Host, User, UserItem
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
    # }------- End of Data Insersions

    session.commit()
    session.close()
    #------- End of Data Submitting ---------



if __name__ == '__main__':
    main()



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
