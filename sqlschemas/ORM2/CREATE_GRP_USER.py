import os
import uuid

#-------[  Import SQLAlchemy ]---------
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence

#-------[  Import From Other Modules   ]---------
from COMMONS import Base, engine, Resource



# ==============================================================
# >>>>>>>>>>>>>>>>>>[    User's ORMs     ] >>>>>>>>>>>>>>>>>>>
# ==============================================================
"""
Explain:
    User's resources could be:
        Account / Track / Albums / Artist / Playlist
    Except for ACCOUNT, it can store the user's login info.
"""



class UserResource(Resource):
    """ [ User Resources are bit different ]
        User items only store ref IDs to REAL resources, like spotify.
    """
    __abstract__ = True

    uri = None
    ref_id = Column('ref_id', String, primary_key=True)



class UserAccount(UserResource):
    """ [ Store all users registered in THIS system ]
        Explain: UserAccount only store users in current system,
        the user which can have multiple binded accounts from other sites.
    """
    __tablename__ = 'u_Accounts'

    password = Column('password', String)
    email = Column('email', String)



class UserTrack(UserResource):
    """ [ User's liked tracks ]
    """
    __tablename__ = 'u_Tracks'

    #uri = Column('uri', String, ForeignKey('references.ref_id'))



class UserAlbum(UserResource):
    """ [ User's saved albums ]
    """
    __tablename__ = 'u_Albums'

    #uri = Column('uri', String, ForeignKey('references.ref_id'))



class UserArtist(UserResource):
    """ [ User's followed artists ]
    """
    __tablename__ = 'u_Artists'

    #uri = Column('uri', String, ForeignKey('references.ref_id'))



class UserPlaylist(UserResource):
    """ [ User's Playlists ]
    """
    __tablename__ = 'u_Playlists'

    #uri = Column('uri', String, ForeignKey('references.ref_id'))






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
        UserAccount.__table__.drop(engine)
        UserTrack.__table__.drop(engine)
        UserAlbum.__table__.drop(engine)
        UserArtist.__table__.drop(engine)
        UserPlaylist.__table__.drop(engine)
        pass
    except Exception as e:
        print('Error on dropping User table.')

    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)

    # Declare a common session for multiple files
    session = sessionmaker(bind=engine, autoflush=False)()


    # Start of Data Insersions --------{
    #import os, json
    #cwd = os.path.split(os.path.realpath(__file__))[0]
    ## Add Hosts
    #with open('{}/hosts.json'.format(os.path.dirname(cwd)), 'r') as f:
    #    data = json.loads( f.read() )
    #hosts = Host.add_sources(session, data['hosts'])
    ## Add a User
    #h1 = session.query(Host).first()
    #with open('{}/spotify/jsondumps-full/get_user_profile.json'.format(os.path.dirname(cwd)), 'r') as f:
    #    data = json.loads( f.read() )

    #User.add(session, h1.id, data)
    # }------- End of Data Insersions

    session.commit()
    session.close()
    #------- End of Data Submitting ---------


if __name__ == '__main__':
    main()
