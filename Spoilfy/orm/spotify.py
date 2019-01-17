#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:
#   - ./common.py


#-------[  Import SQLAlchemy ]---------
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence
from sqlalchemy import exists

#-------[  Import From Other Modules   ]---------
# Package Import Hint: $ python -m Spoilfy.orm.spotify
#-> TEST only
if __name__ in ['__main__', 'spotify']:
    from common import Base, engine, session, Resource
else:
    from orm.common import Base, engine, session, Resource


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

    followers = Column('followers', Integer, default=0)
    images = Column('images', String)
    href = Column('href', String)
    external_urls = Column('external_urls', String)

    def __init__(self, jsondata):
        d = jsondata
        super().__init__(
            uri = d.get('uri'),
            id = d.get('id'),
            type = d.get('type'),
            provider = 'spotify',
            name = d.get('display_name'),
            followers = d.get('followers').get('total'),
            href = d.get('href'),
            images = str( d.get('images') ),
            external_urls = d.get('external_urls',{}).get('spotify'),
        )
        print('[  OK  ] Inserted Spotify User: {}.'.format( self.name ))


class SpotifyTrack(Resource):
    """ [ Track resources in Spotify ]
    """
    __tablename__ = 'spotify_Tracks'

    #-> When is_local=True, the URI is NONE
    is_local = Column('is_local', Boolean)

    albumdata = Column('albumdata', String)
    artistdata = Column('artistdata', String)
    added_at = Column('added_at', Integer)
    disc_number = Column('disc_number', Integer)
    length = Column('length', Integer)
    markets = Column('available_markets', String)
    preview_url = Column('preview_url', String)
    popularity = Column('popularity', Integer)
    explicit = Column('explicit', Boolean)
    href = Column('href', String)
    external_urls = Column('external_urls', String)

    def __init__(self, jsondata):
        # -> Instanize
        d = jsondata.get('track')
        super().__init__(
            # -> Common identifiers
            uri = d.get('uri'),
            name = d.get('name'),
            id = d.get('id'),
            type = d.get('type'),
            provider = 'spotify',
            # -> Spotify specific
            albumdata = str( d.get('album') ),
            artistdata = str( d.get('artists') ),
            is_local = d.get('is_local'),
            added_at = jsondata.get('added_at'),
            disc_number = d.get('disc_number'),
            length = d.get('duration_ms'),
            markets = ','.join( d.get('available_markets') ),
            preview_url = d.get('preview_url'),
            popularity = d.get('popularity'),
            explicit = d.get('explicit'),
            href = d.get('href'),
            external_urls = d.get('external_urls',{}).get('spotify'),
        )



class SpotifyAlbum(Resource):
    """ [ Album resources in Spotify ]
    """
    __tablename__ = 'spotify_Albums'

    trackdata = Column('trackdata', String)
    artistdata = Column('artistdata', String)
    release_date = Column('release_date', String)
    release_date_precision = Column('release_date_precision', String)
    total_tracks = Column('total_tracks', Integer)
    lable = Column('lable', String)
    markets = Column('available_markets', Integer)
    popularity = Column('popularity', Integer)
    copyrights = Column('copyrights', String)
    album_type = Column('album_type', String)
    external_ids = Column('external_ids', String)
    href = Column('href', String)
    external_urls = Column('external_urls', String)


    def __init__(self, jsondata):
        d = jsondata['album']
        super().__init__(
            # -> Common identifiers
            uri = d.get('uri'),
            name = d.get('name'),
            id = d.get('id'),
            type = 'album',
            provider = 'spotify',
            # -> Spotify specific
            trackdata = str( d.get('tracks') ),
            artistdata = str( d.get('artists') ),
            album_type = d.get('album_type',''),
            release_date = d.get('release_date',''),
            release_date_precision = d.get('release_date_precision',''),
            total_tracks = d.get('total_tracks',0),
            lable = d.get('label',''),
            markets = ','.join( d.get('available_markets',[]) ),
            popularity = d.get('popularity'),
            copyrights = str(d.get('copyrights','')),
            href = d.get('href'),
            external_urls = d.get('external_urls',{}).get('spotify',''),
            external_ids = str(d.get('external_ids',{}))
        )




class SpotifyArtist(Resource):
    """ [ Artist resources in Spotify ]
    """
    __tablename__ = 'spotify_Artists'

    genres = Column('genres', String)
    followers = Column('followers', Integer)
    popularity = Column('popularity', Integer)
    href = Column('href', String)
    external_urls = Column('external_urls', String)

    def __init__(self, jsondata):
        d = jsondata
        super().__init__(
            # Common identifiers ->
            uri = d.get('uri'),
            name = d.get('name'),
            id = d.get('id'),
            type = d.get('type'),
            provider = 'spotify',
            # Spotify specific ->
            genres = str(d.get('genres')),
            followers = d.get('followers',{}).get('total'),
            popularity = d.get('popularity'),
            href = d.get('href'),
            external_urls = d.get('external_urls',{}).get('spotify'),
        )



class SpotifyPlaylist(Resource):
    """ [ Playlist resources in Spotify ]
    """
    __tablename__ = 'spotify_Playlists'

    owner_uri = Column('owner_uri', String)
    raw_uri = Column('raw_uri', String)
    snapshot_id = Column('snapshot_id', String)

    total_tracks = Column('total_tracks', Integer)
    followers = Column('followers', Integer)
    collaborative = Column('collaborative', Boolean)
    description = Column('description', String)
    public = Column('public', Boolean)
    images = Column('images', String)
    href = Column('href', String)
    external_urls = Column('external_urls', String)

    def __init__(self, jsondata):
        d = jsondata
        super().__init__(
            # Common identifiers ->
            uri = 'spotify:playlist:{}'.format(d.get('id')),
            name = d.get('name'),
            id = d.get('id'),
            type = d.get('type'),
            provider = 'spotify',
            owner_uri = d.get('owner',{}).get('uri'),
            raw_uri = d.get('uri'),
            # Spotify specific ->
            snapshot_id = d.get('snapshot_id'),
            total_tracks = d.get('tracks',{}).get('total'),
            public = d.get('public'),
            collaborative = d.get('collaborative'),
            images = str(d.get('images')),
            href = d.get('href'),
            external_urls = d.get('external_urls',{}).get('spotify'),
            #-> [Keys below are to be retrieved dynamically]:
            followers = d.get('followers',{}).get('total'),
            description = d.get('description'),
        )



# ==============================================================
# >>>>>>>>>>>>>>>>>>[    TEST RUN     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================



if __name__ == '__main__':
    try:
        # SpotifyAccount.__table__.drop(engine)
        # SpotifyTrack.__table__.drop(engine)
        # SpotifyAlbum.__table__.drop(engine)
        # SpotifyArtist.__table__.drop(engine)
        # SpotifyPlaylist.__table__.drop(engine)
        # Include.__table__.drop(engine)
        pass
    except Exception as e:
        print('Error on dropping Spotify table.')
    finally:
        Base.metadata.create_all(bind=engine)



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
