import os
import uuid

#-------[  Import SQLAlchemy ]---------
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence

#-------[  Import From Other Modules   ]---------
from COMMONS import Base, engine, Resource, Reference



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
        User items only store real IDs to REAL resources, like spotify.
    """
    __tablename__ = 'u_Resources'

    real_uri = Column('real_uri', String, primary_key=True)

    #-> Drop default PK from parent class
    uri = name = id = provider = None  

    @classmethod
    def add(cls, session, data):
        item = cls(
            real_uri=data.real_uri,
            type=data.type
        )
        session.merge(item)
        #session.commit()  #-> Better to commit after multiple inserts
        return item


class UserAccount(Resource):
    """ [ Store all users registered in THIS system ]
        Explain: UserAccount only store users in current system,
        the user which can have multiple binded accounts from other sites.
        Special setting:
            User Account's Real_URI == Reference's URI
            means in Reference, User's reference is himself.
    """
    __tablename__ = 'u_Accounts'

    password = Column('password', String)
    email = Column('email', String)

    @classmethod
    def add(cls, session, data):
        user = cls(
            uri = 'app:user:{}'.format(data['id']),
            name = data['name'],
            id = data['id'],
            type = 'user',
            provider = 'app',
            email = data['email'],
            password = data['password']
        )
        session.merge(user)
        #session.commit()  #-> Better to commit after multiple inserts
        return user




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
        UserResource.__table__.drop(engine)
        pass
    except Exception as e:
        print('Error on dropping User table.')

    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)

    # Declare a common session for multiple files
    session = sessionmaker(bind=engine, autoflush=False)()


    # Start of Data Insersions --------{
    import os, json
    cwd = os.path.split(os.path.realpath(__file__))[0]

    # Add a User Account
    with open('{}/users.json'.format(cwd), 'r') as f:
        jsondata = json.loads( f.read() )
        # Create accounts
        accounts = UserAccount.add_resources(session, jsondata['users'])
        # Initial add reference
        Reference.add_resources(session, accounts)
        # Bind user account to provider accounts
        from CREATE_GRP_SPOTIFY import SpotifyAccount
        app_acc = accounts[0]
        spotify_acc = session.query(SpotifyAccount).filter().first()
        #
        #-> It's critical here we use app account's URI as real_uri
        #   because we want the User Account to be the real existence.
        Reference.bind(session, spotify_acc, app_acc.uri)

    # Add User tracks
    items = session.query(Reference).filter(Reference.type=='track').all()
    UserResource.add_resources(session, items)
    # Add User albums
    items = session.query(Reference).filter(Reference.type=='album').all()
    UserResource.add_resources(session, items)
    # Add User artists
    items = session.query(Reference).filter(Reference.type=='artist').all()
    UserResource.add_resources(session, items)
    # Add User playlists
    items = session.query(Reference).filter(Reference.type=='playlist').all()
    UserResource.add_resources(session, items)


    # }------- End of Data Insersions

    session.commit()
    session.close()
    #------- End of Data Submitting ---------


if __name__ == '__main__':
    main()
