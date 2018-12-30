#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:
#   - ./common.py

import uuid

#-------[  Import SQLAlchemy ]---------
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence

#-------[  Import From Other Modules   ]---------
# Package Import Hint: $ python -m Spoilfy.orm.spotify
from common import Base, engine, Resource, Reference


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

    href = Column('href', String)
    external_urls = Column('external_urls', String)



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
        j = jsondata
        super().__init__(
            uri = j['uri'],
            id = j['id'],
            type = j['type'],
            provider = 'spotify',
            name = j['display_name'],
            external_urls = j['external_urls']['spotify'],
            followers = j['followers']['total'],
            href = j['href'],
            images = str( j['images'] )
        )
        self.session.merge( self )
        print('[  OK  ] Inserted Spotify User: {}.'.format( self.name ))

    @classmethod
    def get_user_by_name(cls, name):
        return cls.query.filter(cls.name == name).first()

    @classmethod
    def get_user_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()



class SpotifyTrack(Resource):
    """ [ Track resources in Spotify ]
    """
    __tablename__ = 'spotify_Tracks'

    album_uri = Column('album_uri', String)
    artist_uris = Column('artist_uris', String)
    #-> When is_local=True, the URI is NONE
    is_local = Column('is_local', Boolean)

    added_at = Column('added_at', Integer)
    disc_number = Column('disc_number', Integer)
    duration_ms = Column('duration_ms', Integer)
    markets = Column('available_markets', String)
    preview_url = Column('preview_url', String)
    popularity = Column('popularity', Integer)
    explicit = Column('explicit', Boolean)
    href = Column('href', String)
    external_urls = Column('external_urls', String)

    def __init__(self, jsondata):
        j = jsondata['track']
        super().__init__(
            uri = j['uri'],
            name = j['name'],
            id = j['id'],
            type = j['type'],
            provider = 'spotify',
            is_local = j['is_local'],
            album_uri = j['album']['uri'],
            artist_uris = ','.join([ a['uri'] for a in j['artists'] ]),
            added_at = jsondata['added_at'],
            disc_number = j['disc_number'],
            duration_ms = j['duration_ms'],
            markets = ','.join([ m for m in j['available_markets'] ]),
            preview_url = j['preview_url'],
            popularity = j['popularity'],
            explicit = j['explicit'],
            href = j['href'],
            external_urls = j['external_urls']['spotify']
        )
        self.session.merge( self )


class SpotifyAlbum(Resource):
    """ [ Album resources in Spotify ]
    """
    __tablename__ = 'spotify_Albums'

    artist_uris = Column('artist_uris', String)
    track_uris = Column('track_uris', String)

    release_date = Column('release_date', String)
    release_date_precision = Column('release_date_precision', String)
    total_tracks = Column('total_tracks', Integer)
    lable = Column('lable', String)
    popularity = Column('popularity', Integer)
    copyrights = Column('copyrights', String)
    album_type = Column('album_type', String)
    external_ids = Column('external_ids', String)
    href = Column('href', String)
    external_urls = Column('external_urls', String)


    def __init__(self, jsondata):
        d = jsondata['album']
        super().__init__(
            uri = d['uri'],
            name = d['name'],
            id = d['id'],
            type = d['type'],
            provider = 'spotify',
            artist_uris = ','.join([ a['uri'] for a in d['artists'] ]),
            track_uris = ','.join([ a['uri'] for a in d['tracks']['items'] ]),
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
        self.session.merge( self )



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
            uri = d['uri'],
            name = d['name'],
            id = d['id'],
            type = d['type'],
            provider = 'spotify',
            genres = str(d['genres']),
            followers = d['followers']['total'],
            popularity = d['popularity'],
            href = d['href'],
            external_urls = str(d['external_urls'])
        )
        self.session.merge( self )   #Merge existing data



class SpotifyPlaylist(Resource):
    """ [ Playlist resources in Spotify ]
    """
    __tablename__ = 'spotify_Playlists'

    owner_uri = Column('owner_uri', String)
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

    def __init__(self, jsondata):
        j = jsondata
        u = j['uri'].split(':')
        super().__init__(
            uri = '{}:{}:{}'.format(u[0],u[3],u[4]),
            name = j['name'],
            id = j['id'],
            type = j['type'],
            provider = 'spotify',
            owner_uri = j['owner']['uri'],
            snapshot_id = j['snapshot_id'],
            total_tracks = j['tracks']['total'],
            public = j['public'],
            collaborative = j['collaborative'],
            images = str(j['images']),
            href = j['href'],
            external_urls = j['external_urls']['spotify'],
            #-> [Keys below are to be retrieved dynamically]:
            #tids = str(j['tracks']['href']),
            #followers = j['followers']['total'],
            #description = j['description'],
        )
        self.session.merge( self )   #Merge existing data
        #-> Temporary: For test only to solve repeated ID issue.
        self.session.commit()  #-> Better to commit after multiple inserts

    @classmethod
    def add_resources(cls, items):
        """[ Add Resources ]
        :param session: sqlalchemy SESSION binded to DB.
        :param LIST items: must be iteratable.
        :return: inserted resource objects.
        """
        all = []
        for item in items:
            data = cls.get_playlist_tracks(item)
            all.append( cls(data) )

        cls.session.commit()
        print('[  OK  ] Inserted {} items to [{}].'.format(
            len(all), cls.__tablename__
        ))

        return all

    @classmethod
    def get_playlist_tracks(cls, item):
        """ [ Get sub item's data through Web API  ]
            This should retrive WebAPI accordingly
            This is to impelemented by children class.
        """
        return item



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
