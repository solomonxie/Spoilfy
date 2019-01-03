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
#-> TEST only
if __name__ in ['__main__', 'spotify']:
    from common import Base, engine, Resource, Reference, Include
else:
    from orm.common import Base, engine, Resource, Reference


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

    album = Column('album', String)
    artists = Column('artists', String)
    #-> When is_local=True, the URI is NONE
    is_local = Column('is_local', Boolean)

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
        d = jsondata.get('track')
        uri = d.get('uri', str(uuid.uuid1()))
        super().__init__(
            # -> Common identifiers
            uri = uri,
            name = d.get('name'),
            id = d.get('id'),
            type = d.get('type'),
            provider = 'spotify',
            # -> Multiple Foreign Keys
            album = self.__bind_album(d.get('album',{}), uri),
            # artists = ','.join([a.get('uri') for a in d.get('artists',[])]),
            artists = self.__add_artists(d.get('artists',[]), uri),
            # -> Spotify specific
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
        self.session.merge( self )

    def __bind_album(self, jsondata, self_uri):
        # Add relationship to [includes] table
        child = Include(jsondata.get('uri'), self_uri, 'album')
        # Also fill up column for current table
        # album = SpotifyAlbum( {'album':jsondata} )
        # self.session.flush()
        # return album.uri
        return jsondata.get('uri')

    def __add_artists(self, jsondata, self_uri):
        # Add relationship to [includes] table
        # children = [Include(self_uri,d.get('uri'),'artist') for d in jsondata]
        # print( '[  OK  ] Included {} albums'.format(len(children)) )
        # Also fill up column for current table
        artists = [ SpotifyArtist(d) for d in jsondata ]
        self.session.flush()
        self.session.commit()
        # return ','.join([ a.uri for a in artists ])
        return ','.join([ a.get('uri') for a in jsondata ])


class SpotifyAlbum(Resource):
    """ [ Album resources in Spotify ]
    """
    __tablename__ = 'spotify_Albums'

    artists = Column('artists', String)
    tracks = Column('tracks', String)

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
        uri = d.get('uri', str(uuid.uuid1()))
        super().__init__(
            # Common identifiers ->
            uri = uri,
            name = d.get('name'),
            id = d.get('id'),
            type = d.get('type'),
            provider = 'spotify',
            # Multiple Foreign Keys ->
            tracks = self.__add_tracks(d, uri),
            artists = self.__add_artists(d.get('artists',[]), uri),
            # Spotify specific ->
            album_type = d.get('album_type'),
            release_date = d.get('release_date'),
            release_date_precision = d.get('release_date_precision'),
            total_tracks = d.get('total_tracks'),
            lable = d.get('label'),
            popularity = d.get('popularity'),
            copyrights = str(d.get('copyrights')),
            href = d.get('href'),
            external_urls = d.get('external_urls',{}).get('spotify'),
            external_ids = str(d.get('external_ids',{}))
        )
        self.session.merge( self )

    def __add_tracks(self, jsondata, self_uri):
        items = jsondata.get('tracks',{}).get('items',[])
        # Add relationship to [includes] table
        children = [ Include(self_uri, d.get('uri'), 'album') for d in items ]
        # print( '[  OK  ] Included {} tracks'.format(len(children)) )
        # Also fill up column for current table
        # tracks = [ SpotifyTrack({'track':d}) for d in jsondata ]
        # return ','.join([ t.uri for t in tracks ])
        return ','.join([ t.get('uri') for t in items ])

    def __add_artists(self, jsondata, self_uri):
        # Add relationship to [includes] table
        children = [Include(d.get('uri'),self_uri,'artist') for d in jsondata]
        # print( '[  OK  ] Included {} albums'.format(len(children)) )
        # Also fill up column for current table
        # artists = [ SpotifyArtist(d) for d in jsondata ]
        # self.session.flush()
        # return ','.join([ a.uri for a in artists ])
        return ','.join([ a.get('uri') for a in jsondata ])


class SpotifyArtist(Resource):
    """ [ Artist resources in Spotify ]
    """
    __tablename__ = 'spotify_Artists'

    albums = Column('albums', String)

    genres = Column('genres', String)
    followers = Column('followers', Integer)
    popularity = Column('popularity', Integer)
    href = Column('href', String)
    external_urls = Column('external_urls', String)

    def __init__(self, jsondata):
        d = jsondata
        super().__init__(
            # Common identifiers ->
            uri = d.get('uri', str(uuid.uuid1())),
            name = d.get('name'),
            id = d.get('id'),
            type = d.get('type'),
            provider = 'spotify',
            # Multiple Foreign Keys ->
            albums = self.__add_albums({}),
            # Spotify specific ->
            genres = str(d.get('genres')),
            followers = d.get('followers',{}).get('total'),
            popularity = d.get('popularity'),
            href = d.get('href'),
            external_urls = d.get('external_urls',{}).get('spotify'),
        )
        self.session.merge( self )   #Merge existing data

    def __add_albums(self, jsondata):
        return str(jsondata)



class SpotifyPlaylist(Resource):
    """ [ Playlist resources in Spotify ]
    """
    __tablename__ = 'spotify_Playlists'

    owner_uri = Column('owner_uri', String)
    snapshot_id = Column('snapshot_id', String)
    tids = Column('track_ids', String)
    tracks = Column('tracks', String)

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
        u = d.get('uri','').split(':')
        super().__init__(
            # Common identifiers ->
            uri = '{}:{}:{}'.format(u[0],u[3],u[4]),
            name = d.get('name'),
            id = d.get('id'),
            type = d.get('type'),
            provider = 'spotify',
            owner_uri = d.get('owner',{}).get('uri'),
            # Multiple Foreign Keys ->
            tracks = self.__add_tracks({}),
            # Spotify specific ->
            snapshot_id = d.get('snapshot_id'),
            total_tracks = d.get('tracks',{}).get('total'),
            public = d.get('public'),
            collaborative = d.get('collaborative'),
            images = str(d.get('images')),
            href = d.get('href'),
            external_urls = d.get('external_urls',{}).get('spotify'),
            #-> [Keys below are to be retrieved dynamically]:
            tids = str(d.get('tracks',{}).get('href')),
            followers = d.get('followers',{}).get('total'),
            description = d.get('description'),
        )
        self.session.merge( self )   #Merge existing data
        #-> Temporary: For test only to solve repeated ID issue.
        self.session.commit()  #-> Better to commit after multiple inserts

    def __add_tracks(self, jsondata):
        return str(jsondata)

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
