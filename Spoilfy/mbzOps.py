#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import uuid
import json

#-------[  Import From Other Modules   ]---------
#-> TEST only
if __name__ in ['__main__', 'mbzOps']:
    from orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    from orm.common import Base, engine, session
    from orm.common import Resource, Reference, Include
    import webapi.apiMusicbrainz as MbzAPI
else:
    # Package Import Hint: $ python -m Spoilfy.orm.musicbrainz
    from Spoilfy.orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    from Spoilfy.orm.common import Base, engine, session
    from Spoilfy.orm.common import Resource, Reference, Include



# ==============================================================
# >>>>>>>>>>>>>>>[    Operator Classes     ] >>>>>>>>>>>>>>>>>
# ==============================================================


class MbzOps:
    """ [ Musicbrainz Operations Base Class ]

    """

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


class MbzOpsTrack(MbzOps):
    """ [ Musicbrainz Track Operations ]

    """
    ORM = MusicbrainzTrack

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



class MbzOpsAlbum(MbzOps):
    """ [ Musicbrainz Album Operations ]

    """
    ORM = MusicbrainzAlbum

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



class MbzOpsArtist(MbzOps):
    """ [ Musicbrainz Artist Operations ]

    """
    ORM = MusicbrainzArtist

    @classmethod
    def loads(cls, jsondata):
        # Insert items to DB
        items = MusicbrainzArtist.add_resources(jsondata.get('artists',{}))
        # Make NEW reference
        Reference.add_resources(items)







