#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:
#   - ./common.py

import uuid

#-------[  Import SQLAlchemy ]---------
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence
from sqlalchemy import exists

#-------[  Import From Other Modules   ]---------
# Package Import Hint: $ python -m Spoilfy.orm.musicbrainz

#-> TEST only
if __name__ in ['__main__', 'musicbrainz']:
    from common import Base, engine, session, Resource, Reference, Include
else:
    from orm.common import Base, engine, session, Resource, Reference, Include


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

    @classmethod
    def load(cls, jsondata, real_uri):
        # Add ONE item to database
        mbz = session.merge( cls(jsondata) )
        print( '\t[INSERT]', mbz )
        # Bind reference
        ref = Reference(mbz, real_uri, mbz.score/100)
        print( '\t[BIND]', ref, ' at ', ref.real_uri )
        session.merge( ref )
        session.commit()
        return mbz


class MusicbrainzTrack(MusicbrainzResource):
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

    @classmethod
    def loads(cls, jsondata):
        # Insert items to DB
        items = MusicbrainzTrack.add_resources(jsondata['recordings'])
        # Add NEW NEW NEW reference
        Reference.add_resources(items)
        # Bind each track's [albums] & [artists]
        for track in jsondata['recordings']:
            MusicbrainzTrack.include_albums( track )
            MusicbrainzTrack.include_artists( track )

    @classmethod
    def get_sub_ids(cls, trackdata):
        album_ids  = [ a.get('id')
                for a in trackdata.get('releases', []) ]
        artist_ids = [ a.get('artist', {}).get('id')
                for a in trackdata.get('artist-credit', []) ]
        return album_ids, artist_ids

    @classmethod
    def include_albums(cls, trackdata):
        child = 'musicbrainz:track:{}'.format( trackdata.get('id') )
        for album in trackdata.get('releases', []):
            parent = 'musicbrainz:album:{}'.format( album.get('id') )
            #->
            inc = session.merge( Include(parent, child) )
            print( '[INCLUDE:TRACK-ALBUM]', parent, child )
        # Submit changes
        session.commit()

    @classmethod
    def include_artists(cls, trackdata):
        child = 'musicbrainz:track:{}'.format( trackdata.get('id') )
        for r in trackdata.get('artist-credit', []):
            parent = 'musicbrainz:artist:' + r.get('artist',{}).get('id')
            # ->
            inc = session.merge( Include(parent, child) )
            print( '[INCLUDE:TRACK-ARTIST]', parent, child )
        # Submit changes
        session.commit()


class MusicbrainzAlbum(MusicbrainzResource):
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

    @classmethod
    def loads(cls, jsondata):
        # Insert items to DB
        items = MusicbrainzAlbum.add_resources(jsondata.get('releases',{}))
        # Make NEW NEW NEW reference
        Reference.add_resources(items)
        # Bind each album's [artists] & [tracks]
        for album in jsondata['releases']:
            MusicbrainzAlbum.include_artists( album )

    @classmethod
    def get_sub_ids(cls, albumdata):
        track_ids  = []
        artist_ids = [ a.get('artist', {}).get('id')
                for a in albumdata.get('artist-credit', []) ]
        return track_ids, artist_ids

    @classmethod
    def include_artists(cls, albumdata):
        child = 'musicbrainz:album:{}'.format( albumdata.get('id') )
        for r in albumdata.get('artist-credit', []):
            parent = 'musicbrainz:artist:' + r.get('artist',{}).get('id')
            # ->
            inc = session.merge( Include(parent, child) )
            print( '[INCLUDE:ALBUM-ARTIST]', parent, child )
        # Submit changes
        session.commit()


class MusicbrainzArtist(MusicbrainzResource):
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

    @classmethod
    def loads(cls, jsondata):
        # Insert items to DB
        items = MusicbrainzArtist.add_resources(jsondata.get('artists',{}))
        # Make NEW reference
        Reference.add_resources(items)



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
