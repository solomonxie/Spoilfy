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

#-> TEST only
if __name__ == '__main__':
    from common import Base, engine, Resource, Reference
else:
    from orm.common import Base, engine, Resource, Reference


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


class MusicbrainzTrack(Resource):
    """ [ Track resources in Musicbrainz ]
    """
    __tablename__ = 'mbz_Tracks'

    releases = Column('releases', String)
    artist_credit = Column('artist_credit', String)

    length = Column('length', Integer)
    score = Column('score', String)
    video = Column('video', String)

    def __init__(self, data):
        d = data
        super().__init__(
            uri = 'musicbrainz:track:{}'.format( d.get('id') ),
            id = d.get('id'),
            type = 'track',
            provider = 'musicbrainz',
            name = d.get('title'),
            artist_credit = str(d.get('artist-credit')),
            releases = str(d.get('releases')),
            score = d.get('score'),
            length = d.get('length'),
            video = d.get('video'),
        )
        self.session.merge( self )


class MusicbrainzAlbum(Resource):
    """ [ Album resources in Musicbrainz ]
    """
    __tablename__ = 'mbz_Albums'

    artist_credit = Column('artist_credit', String)
    track_uris = Column('track_uris', String)

    score = Column('score', Integer)
    track_count = Column('track_count', Integer)
    status = Column('status', String)
    country = Column('country', String)
    date = Column('date', String)
    release_events = Column('release_events', String)
    release_group = Column('release_group', String)
    barcode = Column('barcode', String)
    count = Column('count', Integer)
    label_info = Column('label_info', String)
    media = Column('media', String)
    text_representation = Column('text_representation', String)


    def __init__(self, jsondata):
        d = jsondata
        super().__init__(
            uri = 'musicbrainz:album:{}'.format( d.get('id') ),
            name = d.get('title'),
            id = d.get('id'),
            type = 'album',
            provider = 'musicbrainz',
            track_uris = None,
            artist_credit = str(d.get('artist-credit')),
            score = d.get('score'),
            track_count = d.get('track-count'),
            status = d.get('status'),
            country = d.get('country'),
            date = d.get('date'),
            release_events = str(d.get('release-events')),
            release_group = str(d.get('release-group')),
            barcode = d.get('barcode'),
            count = d.get('count'),
            label_info = str(d.get('label-info')),
            media = str(d.get('media')),
            text_representation = str(d.get('text-representation')),
        )
        self.session.merge( self )



class MusicbrainzArtist(Resource):
    """ [ Artist resources in Musicbrainz ]
    """
    __tablename__ = 'mbz_Artists'

    artist_type = Column('artist_type', String)
    artist_type_id = Column('artist_type_id', String)
    score = Column('score', String)
    sort_name = Column('sort_name', String)
    aliases = Column('aliases', String)
    area = Column('area', String)
    begin_area = Column('begin_area', String)
    country = Column('country', String)
    disambiguation = Column('disambiguation', String)
    lifespan = Column('lifespan', String)
    tags = Column('tags', String)

    def __init__(self, jsondata):
        d = jsondata
        super().__init__(
            uri = 'musicbrainz:artist:{}'.format( d.get('id') ),
            name = d.get('name'),
            id = d.get('id'),
            type = 'artist',
            provider = 'musicbrainz',
            artist_type = d.get('type'),
            artist_type_id = d.get('type-id'),
            score = d.get('score'),
            sort_name = d.get('sort-name'),
            aliases = str(d.get('aliases')),
            area = str(d.get('area')),
            begin_area = str(d.get('begin-area')),
            country = d.get('country'),
            disambiguation = d.get('disambiguation'),
            lifespan = str(d.get('lifespan')),
            tags = str(d.get('tags')),
        )
        self.session.merge( self )   #Merge existing data




print('[  OK  ] __IMPORTED__: {}'.format(__name__))
