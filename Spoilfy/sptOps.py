#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json

from sqlalchemy.orm import aliased

#-------[  Import From Other Modules   ]---------
#-> TEST only
if __name__ in ['__main__', 'sptOps']:
    from orm.spotify import *
    from orm.musicbrainz import *
    from orm.common import Base, engine, session
    from orm.common import Resource, Reference, Include
    from webapi.apiSpotify import SpotifyAPI
    import webapi.apiMusicbrainz as MbzAPI
else:
    # Package Import Hint: $ python -m Spoilfy.orm.spotify
    from Spoilfy.orm.spotify import *
    from Spoilfy.orm.musicbrainz import *
    from Spoilfy.orm.common import Base, engine, session
    from Spoilfy.orm.common import Resource, Reference, Include
    from Spoilfy.webapi.apiSpotify import SpotifyAPI
    import Spoilfy.webapi.apiMusicbrainz as MbzAPI



# ==============================================================
# >>>>>>>>>>>>>>>[    Operator Classes     ] >>>>>>>>>>>>>>>>>
# ==============================================================

with open('./webapi/.spotify_app.json', 'r') as f:
    _data = json.loads( f.read() )


class SptOps:

    ORM = None
    API = SpotifyAPI(_data)




class SptOpsAccount(SptOps):
    """ [ Spotify Account Operations ]

    """
    ORM = SpotifyAccount

    @classmethod
    def get_user_by_name(cls, name):
        return cls.ORM.query.filter(cls.ORM.name == name).first()

    @classmethod
    def get_user_by_id(cls, id):
        return cls.ORM.query.filter(cls.ORM.id == id).first()

    @classmethod
    def get_my_profile(cls):
        return SptOpsAccount.load( cls.API.get_my_profile() )

    @classmethod
    def load(cls, jsondata):
        # Insert items to DB
        user = session.merge( cls.ORM(jsondata) )
        # Add reference
        session.merge( Reference(user) )
        session.commit()
        return user



class SptOpsTrack(SptOps):
    """ [ Spotify Track Operations ]

    """
    ORM = SpotifyTrack

    @classmethod
    def load(cls, jsondata):
        track = session.merge( cls.ORM(jsondata) )
        ref = session.merge( Reference(track) )
        session.commit()
        return ref

    @classmethod
    def loads(cls, jsondata):
        all = []
        for o in jsondata.get('items', []):
            all.append( cls.load(o) )
            cls.include_album(o)
            cls.include_artists(o)
        return all

    #-----------------------------------------#

    @classmethod
    def include_album(cls, trackdata):
        track = trackdata.get('track',{})
        child = track.get('uri', '')
        parent = track.get('album', {}).get('uri', '')
        inc = session.merge( Include(parent, child) )
        session.commit()
        return inc

    @classmethod
    def include_artists(cls, trackdata):
        track = trackdata.get('track', {})
        child = track.get('uri')

        for r in track.get('artists', []):
            parent = r.get('uri')
            inc = session.merge( Include(parent, child) )
        session.commit()




class SptOpsAlbum(SptOps):
    """ [ Spotify Album Operations ]

    """
    ORM = SpotifyAlbum

    @classmethod
    def load(cls, jsondata):
        album = session.merge( cls.ORM(jsondata) )
        ref = session.merge( Reference(album) )
        session.commit()
        return ref

    @classmethod
    def loads(cls, jsondata):
        all = []
        for o in jsondata.get('items', []):
            all.append( cls.load(o) )
            cls.include_tracks(o)
            cls.include_artists(o)
        return all

    #------------------------------------------#

    @classmethod
    def include_tracks(cls, albumdata):
        album = albumdata.get('album', {})
        parent = album.get('uri')

        for page in cls.API.get_album_tracks(album.get('id')):
            for o in page.get('items', []):
                child = o.get('uri')
                if child:
                    inc = session.merge( Include(parent, child) )
                    SptOpsTrack.include_artists(albumdata)
            session.commit()
            # break


    @classmethod
    def include_artists(cls, albumdata):
        album = albumdata.get('album', {})
        child = album.get('uri')

        for r in album.get('artists', []):
            parent = r.get('uri')
            inc = session.merge( Include(parent, child) )

        session.commit()



class SptOpsArtist(SptOps):
    """ [ Spotify Artist Operations ]

    """
    ORM = SpotifyArtist

    @classmethod
    def load(cls, jsondata):
        album = session.merge( cls.ORM(jsondata) )
        ref = session.merge( Reference(album) )
        session.commit()
        return ref

    @classmethod
    def loads(cls, jsondata):
        return [cls.load(o) for o in jsondata.get('artists',{}).get('items',[])]




class SptOpsPlaylist(SptOps):
    """ [ Spotify Playlist Operations ]

    """
    ORM = SpotifyPlaylist

    @classmethod
    def load(cls, jsondata):
        playlist = session.merge( cls.ORM(jsondata) )
        ref = session.merge( Reference(playlist) )
        session.commit()
        return ref

    @classmethod
    def loads(cls, jsondata):
        all = []
        for o in jsondata.get('items', []):
            all.append( cls.load(o) )
            cls.include_tracks(o)
        return all

    #-----------------------------------------------#

    @classmethod
    def include_tracks(cls, playlistdata):
        parent = 'spotify:playlist:{}'.format( playlistdata.get('id') )
        # original playlist uri: "spotify:user:xxxxxxxx:playlist:xxxxxxx"

        for page in cls.API.get_playlist_tracks(playlistdata.get('id')):
            for o in page.get('items', []):
                child = o.get('track',{}).get('uri')
                if child:
                    inc = session.merge( Include(parent, child) )
                    session.commit()
            # break




class SptOpsMissing(SptOps):
    """ [ Search/Fetch for missing data ]
    """

    @classmethod
    def _find_missing(cls, sql):
        with engine.connect() as con:
            records = con.execute(sql)
            uris = [ u for u, in records ]
        return uris

    @classmethod
    def find_missing_tracks(cls):
        return cls._find_missing(
            """
            SELECT child_uri FROM includes
                WHERE child_type='track' AND provider='spotify'
                AND (parent_type='album' OR parent_type='playlist')
                AND child_uri NOT IN (SELECT uri FROM spotify_Tracks)
                GROUP BY child_uri
            """
        )

    @classmethod
    def find_missing_albums(cls):
        return cls._find_missing(
            """
            SELECT parent_uri FROM includes
                WHERE parent_type='album' AND provider='spotify'
                AND parent_uri NOT IN (SELECT uri FROM spotify_Albums)
                GROUP BY parent_uri
            """
        )

    @classmethod
    def find_missing_artists(cls):
        return cls._find_missing(
            """
            SELECT parent_uri FROM includes
                WHERE parent_type='artist' AND provider='spotify'
                AND parent_uri NOT IN (SELECT uri FROM spotify_Artists)
                GROUP BY parent_uri
            """
        )

    #---------------------------------------------------------#

    @classmethod
    def fix_missing_tracks(cls):
        refs = []
        missings = cls.find_missing_tracks()
        print( '[ FIX ] {} missing TRACKS...'.format(len(missings)) )

        for i,uri in enumerate(missings):
            print( i+1 )
            t = cls.API.get_a_track( uri.split(':')[2] )
            if t:
                track = session.merge(SpotifyTrack( {'track':t} ))
                refs.append( session.merge(Reference( track )) )
                session.commit()

        print('\t[ GET ] {}/{} Missing track.'.format(len(refs),len(missings)))

        return refs

    @classmethod
    def fix_missing_albums(cls):
        refs = []
        missings = cls.find_missing_albums()
        print( '[ FIX ] {} missing ALBUMS...'.format(len(missings)) )

        for i,uri in enumerate(missings):
            print( i+1 )
            albumdata = {'album': cls.API.get_a_album( uri.split(':')[2] )}
            album = session.merge(SpotifyAlbum( albumdata ))
            refs.append( session.merge(Reference( album )) )
            session.commit()

        print('\t[ GET ] {}/{} albums.'.format(len(refs),len(missings)))

        return refs

    @classmethod
    def fix_missing_artists(cls):
        refs = []
        missings = cls.find_missing_artists()
        print( '[ FIX ] {} missing ARTISTS...'.format(len(missings)) )

        for i,uri in enumerate(missings):
            print( i+1 )
            artistdata = cls.API.get_a_artist( uri.split(':')[2] )
            artist = session.merge(SpotifyArtist( artistdata ))
            refs.append( session.merge(Reference( artist )) )
            session.commit()

        print('\t[ GET ]{}/{} artists.'.format(len(refs),len(missings)))

        return refs

