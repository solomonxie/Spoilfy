import os
import uuid

#-------[  Import SQLAlchemy ]---------
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence

#-------[  Import From Other Modules   ]---------
from COMMONS import Base, engine, Resource



# ==============================================================
# >>>>>>>>>>>[    Provider's ORMs [Spotify]     ] >>>>>>>>>>>>>>
# ==============================================================
"""
Provider:
    Spotify is a [MediaProvider].
Explain:
"""


class SpotifyAccount(Resource):
    """ [ Store User Accounts with Spotify ]
        Information might involve with Authentication / Password.
    """
    __tablename__ = 'spotify_Accounts'

    password = Column('password', String)
    email = Column('email', String)



class SpotifyTrack(Resource):
    """ [ Track resources in Spotify ]
    """
    __tablename__ = 'spotify_Tracks'

    #uri = Column('uri', String, ForeignKey('references.ref_id'))



class SpotifyAlbum(Resource):
    """ [ Album resources in Spotify ]
    """
    __tablename__ = 'spotify_Albums'

    #uri = Column('uri', String, ForeignKey('references.ref_id'))



class SpotifyArtist(Resource):
    """ [ Artist resources in Spotify ]
    """
    __tablename__ = 'spotify_Artists'

    #uri = Column('uri', String, ForeignKey('references.ref_id'))



class SpotifyPlaylist(Resource):
    """ [ Playlist resources in Spotify ]
    """
    __tablename__ = 'spotify_Playlists'

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
        SpotifyAccount.__table__.drop(engine)
        SpotifyTrack.__table__.drop(engine)
        pass
    except Exception as e:
        print('Error on dropping Spotify table.')

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
    ## Add a Spotify
    #h1 = session.query(Host).first()
    #with open('{}/spotify/jsondumps-full/get_user_profile.json'.format(os.path.dirname(cwd)), 'r') as f:
    #    data = json.loads( f.read() )

    #Spotify.add(session, h1.id, data)
    # }------- End of Data Insersions

    session.commit()
    session.close()
    #------- End of Data Submitting ---------


if __name__ == '__main__':
    main()

