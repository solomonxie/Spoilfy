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
# Package Import Hint: $ python -m Spoilfy.orm.musicbrainz
from common import Base, engine, Resource, Reference


# ==============================================================
# >>>>>>>>>>>[    Provider's ORMs [Musicbrainz]     ] >>>>>>>>>>
# ==============================================================
"""
Provider:
    Musicbrainz is a [InfoProvider].
Explain:
"""


class MusicbrainzResource(Resource):
    __abstract__ = True

    href = Column('href', String)
    external_urls = Column('external_urls', String)



class MusicbrainzAccount(Resource):
    """ [ Store User Accounts with Musicbrainz ]
        Information might involve with Authentication / Password.
    """
    __tablename__ = 'mbz_Accounts'

    @classmethod
    def add(cls, jsondata):
        user = cls(
            uri = jsondata['uri'],
            id = jsondata['id'],
            type = jsondata['type'],
            provider = 'musicbrainz',
            name = jsondata['name']
        )
        cls.session.merge(user)
        # cls.session.commit()
        print('[  OK  ] Inserted Musicbrainz User: {}.'.format(user.name))

        return user



class MusicbrainzTrack(Resource):
    """ [ Track resources in Musicbrainz ]
    """
    __tablename__ = 'mbz_Tracks'

    atids = Column('atids', String)
    abids = Column('abids', String)

    score = Column('score', Integer)
    length = Column('length', Integer)

    @classmethod
    def add(cls, jsondata):
        j = jsondata['recording']
        item = cls(
            uri = j['uri'],
            name = j['title'],
            id = j['id'],
            type = 'track',
            provider = 'musicbrainz',
        )
        cls.session.merge( item )   #Merge existing data
        #cls.session.commit()  #-> Better to commit after multiple inserts

        return item


class MusicbrainzAlbum(Resource):
    """ [ Album resources in Musicbrainz ]
    """
    __tablename__ = 'mbz_Albums'

    atids = Column('artist_ids', String)
    tids = Column('track_ids', String)

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



    @classmethod
    def add(cls, jsondata):
        d = jsondata['album']
        item = cls(
            uri = d['uri'],
            name = d['name'],
            id = d['id'],
            type = d['type'],
            provider = 'musicbrainz',
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
        cls.session.merge( item )
        #cls.session.commit()  #-> Better to commit after multiple inserts
        return item



class MusicbrainzArtist(Resource):
    """ [ Artist resources in Musicbrainz ]
    """
    __tablename__ = 'mbz_Artists'

    genres = Column('genres', String)
    followers = Column('followers', Integer)
    popularity = Column('popularity', Integer)
    href = Column('href', String)
    external_urls = Column('external_urls', String)


    @classmethod
    def add(cls, jsondata):
        d = jsondata
        item = cls(
            uri = d['uri'],
            name = d['name'],
            id = d['id'],
            type = d['type'],
            provider = 'musicbrainz',
            genres = str(d['genres']),
            followers = d['followers']['total'],
            popularity = d['popularity'],
            href = d['href'],
            external_urls = str(d['external_urls'])
        )
        cls.session.merge( item )   #Merge existing data
        #cls.session.commit()  #-> Better to commit after multiple inserts
        return item



class MusicbrainzPlaylist(Resource):
    """ [ Playlist resources in Musicbrainz ]
    """
    __tablename__ = 'mbz_Playlists'

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
    def add(cls, jsondata):
        j = jsondata
        u = j['uri'].split(':')
        item = cls(
            uri = '{}:{}:{}'.format(u[0],u[3],u[4]),
            name = j['name'],
            id = j['id'],
            type = j['type'],
            provider = 'musicbrainz',
            owner_id = j['owner']['id'],
            snapshot_id = j['snapshot_id'],
            total_tracks = j['tracks']['total'],
            public = j['public'],
            collaborative = j['collaborative'],
            images = str(j['images']),
            href = j['href'],
            external_urls = j['external_urls']['musicbrainz'],
            #-> [Keys below are to be retrieved dynamically]:
            #tids = str(j['tracks']['href']),
            #followers = j['followers']['total'],
            #description = j['description'],
        )
        cls.session.merge( item )   #Merge existing data
        #-> Temporary: For test only to solve repeated ID issue.
        cls.session.commit()  #-> Better to commit after multiple inserts
        return item

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
            obj = cls.add(data)
            all.append( obj )

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
