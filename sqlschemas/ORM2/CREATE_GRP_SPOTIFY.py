import os
import uuid

#-------[  Import SQLAlchemy ]---------
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence

#-------[  Import From Other Modules   ]---------
from COMMONS import Base, engine, Resource, Reference



# ==============================================================
# >>>>>>>>>>>[    Provider's ORMs [Spotify]     ] >>>>>>>>>>>>>>
# ==============================================================
"""
Provider:
    Spotify is a [MediaProvider].
Explain:
"""


class SpotifyResource(Resource):
    __abstract__ = True

    provider_name = 'spotify'


class SpotifyAccount(SpotifyResource):
    """ [ Store User Accounts with Spotify ]
        Information might involve with Authentication / Password.
    """
    __tablename__ = 'spotify_Accounts'

    name = Column('name', String)
    external_urls = Column('external_urls', String)
    followers = Column('followers', Integer, default=0)
    href = Column('href', String)
    images = Column('images', String)

    @classmethod
    def add(cls, session, jsondata):
        user = cls(
            uri = jsondata['uri'],
            id = jsondata['id'],
            type = jsondata['type'],
            provider = cls.provider_name,
            name = jsondata['display_name'],
            external_urls = jsondata['external_urls']['spotify'],
            followers = jsondata['followers']['total'],
            href = jsondata['href'],
            images = str(jsondata['images'])
        )
        session.merge(user)
        session.commit()
        print('[  OK  ] Inserted Spotify User: {}.'.format( user.name ))

        return user



class SpotifyTrack(SpotifyResource):
    """ [ Track resources in Spotify ]
    """
    __tablename__ = 'spotify_Tracks'

    atids = Column('artist_ids', String)
    #-> When is_local=True, the URI is NONE
    is_local = Column('is_local', Boolean)

    disc_number = Column('disc_number', Integer)
    duration_ms = Column('duration_ms', Integer)
    markets = Column('available_markets', String)
    preview_url = Column('preview_url', String)
    popularity = Column('popularity', Integer)
    explicit = Column('explicit', Boolean)
    href = Column('href', String)
    external_urls = Column('external_urls', String)


    @classmethod
    def add(cls, session, jsondata):
        j = jsondata['track']
        item = cls(
            uri = j['uri'],
            name = j['name'],
            id = j['id'],
            type = j['type'],
            provider = cls.provider_name,
            is_local = j['is_local'],
            atids = ','.join([ a['id'] for a in j['artists'] ]),
            disc_number = j['disc_number'],
            duration_ms = j['duration_ms'],
            markets = ','.join([ m for m in j['available_markets'] ]),
            preview_url = j['preview_url'],
            popularity = j['popularity'],
            explicit = j['explicit'],
            href = j['href'],
            external_urls = j['external_urls']['spotify']
        )
        session.merge( item )   #Merge existing data
        #session.commit()  #-> Better to commit after multiple inserts

        return item


class SpotifyAlbum(SpotifyResource):
    """ [ Album resources in Spotify ]
    """
    __tablename__ = 'spotify_Albums'

    atids = Column('artist_ids', String)
    tids = Column('track_ids', String)

    release_date = Column('release_date', String)
    release_date_precision = Column('release_date_precision', String)
    total_tracks = Column('total_tracks', Integer)
    lable = Column('lable', String)
    popularity = Column('popularity', Integer)
    copyrights = Column('copyrights', String)
    album_type = Column('album_type', String)
    href = Column('href', String)
    external_urls = Column('external_urls', String)
    external_ids = Column('external_ids', String)


    @classmethod
    def add(cls, session, jsondata):
        d = jsondata['album']
        item = cls(
            uri = d['uri'],
            name = d['name'],
            id = d['id'],
            type = d['type'],
            provider = cls.provider_name,
            atids = ','.join([ a['id'] for a in d['artists'] ]),
            tids = ','.join([ a['id'] for a in d['tracks']['items'] ]),
            album_type = d['album_type'],
            release_date = d['release_date'],
            release_date_precision = d['release_date_precision'],
            total_tracks = d['total_tracks'],
            lable = d['label'],
            popularity = d['popularity'],
            copyrights = str(d['copyrights']),
            href = d['href'],
            external_urls = str(d['external_urls']),
            external_ids = str(d['external_ids'])
        )
        session.merge( item )
        #session.commit()  #-> Better to commit after multiple inserts
        return item



class SpotifyArtist(SpotifyResource):
    """ [ Artist resources in Spotify ]
    """
    __tablename__ = 'spotify_Artists'

    genres = Column('genres', String)
    followers = Column('followers', Integer)
    popularity = Column('popularity', Integer)
    href = Column('href', String)
    external_urls = Column('external_urls', String)


    @classmethod
    def add(cls, session, jsondata):
        d = jsondata
        item = cls(
            uri = d['uri'],
            name = d['name'],
            id = d['id'],
            type = d['type'],
            provider = cls.provider_name,
            genres = str(d['genres']),
            followers = d['followers']['total'],
            popularity = d['popularity'],
            href = d['href'],
            external_urls = str(d['external_urls'])
        )
        session.merge( item )   #Merge existing data
        #session.commit()  #-> Better to commit after multiple inserts
        return item



class SpotifyPlaylist(SpotifyResource):
    """ [ Playlist resources in Spotify ]
    """
    __tablename__ = 'spotify_Playlists'

    owner_id = Column('owner_id', String)
    snapshot_id = Column('snapshot_id', String)
    tids = Column('track_ids', String)

    total_tracks = Column('total_tracks', Integer)
    followers = Column('followers', Integer)
    collaborative = Column('collaborative', Boolean)
    description = Column('description', String)
    public = Column('public', Boolean)
    images = Column('images', String)
    href = Column('href', String)
    external_urls = Column('external_urls', String)

    @classmethod
    def add(cls, session, jsondata):
        j = jsondata
        u = j['uri'].split(':')
        item = cls(
            uri = '{}:{}:{}'.format(u[0],u[3],u[4]),
            name = j['name'],
            id = j['id'],
            type = j['type'],
            provider = cls.provider_name,
            owner_id = j['owner']['id'],
            snapshot_id = j['snapshot_id'],
            total_tracks = j['tracks']['total'],
            public = j['public'],
            collaborative = j['collaborative'],
            images = str(j['images']),
            href = j['href'],
            external_urls = j['external_urls']['spotify'],
            #-> [Keys below are to be retireved from WebAPI]:
            #tids = str(j['tracks']['href']),
            #followers = j['followers']['total'],
            #description = j['description'],
        )
        session.merge( item )   #Merge existing data
        #-> Temporary: For test only to solve reeated ID issue.
        session.commit()  #-> Better to commit after multiple inserts
        return item





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
        SpotifyAlbum.__table__.drop(engine)
        SpotifyArtist.__table__.drop(engine)
        SpotifyPlaylist.__table__.drop(engine)
        pass
    except Exception as e:
        print('Error on dropping Spotify table.')

    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)

    # Declare a common session for multiple files
    session = sessionmaker(bind=engine, autoflush=False)()


    # Start of Data Insersions --------{
    import os, json
    cwd = os.path.split(os.path.realpath(__file__))[0]

    # Add an account
    with open('{}/spotify/jsondumps-full/get_user_profile.json'.format(os.path.dirname(cwd)), 'r') as f:
        jsondata = json.loads( f.read() )
        # Create items
        items = SpotifyAccount.add(session, jsondata)
        # Add reference

    # Add a track
    with open('{}/spotify/jsondumps-full/get_user_tracks.json'.format(os.path.dirname(cwd)), 'r') as f:
        jsondata = json.loads( f.read() )
        # Create items
        items = SpotifyTrack.add_resources(session, jsondata['items'])
        # Add reference
        Reference.add_resources(session, items)

    # Add an album
    with open('{}/spotify/jsondumps-full/get_user_albums.json'.format(os.path.dirname(cwd)), 'r') as f:
        jsondata = json.loads( f.read() )
        items = SpotifyAlbum.add_resources(session, jsondata['items'])
        # Add reference
        Reference.add_resources(session, items)

    # Add an artist
    with open('{}/spotify/jsondumps-full/get_user_artists.json'.format(os.path.dirname(cwd)), 'r') as f:
        jsondata = json.loads( f.read() )
        items = SpotifyArtist.add_resources(session, jsondata['artists']['items'])
        # Add reference
        Reference.add_resources(session, items)

    # Add a playlist
    with open('{}/spotify/jsondumps-full/get_user_playlists.json'.format(os.path.dirname(cwd)), 'r') as f:
        jsondata = json.loads( f.read() )
        items = SpotifyPlaylist.add_resources(session, jsondata['items'])
        # Add reference
        Reference.add_resources(session, items)

    # }------- End of Data Insersions

    session.commit()
    session.close()
    #------- End of Data Submitting ---------


if __name__ == '__main__':
    main()

