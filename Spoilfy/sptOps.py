#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json

#-------[  Import From Other Modules   ]---------
#-> TEST only
if __name__ in ['__main__', 'sptOps']:
    from orm.spotify import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist, SpotifyAccount
    from orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    from orm.common import Base, engine, session
    from orm.common import Resource, Reference, Include
    from webapi.apiSpotify import SpotifyAPI
    import webapi.apiMusicbrainz as MbzAPI
else:
    # Package Import Hint: $ python -m Spoilfy.orm.spotify
    from Spoilfy.orm.spotify import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist, SpotifyAccount
    from Spoilfy.orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
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
    API = SpotifyAPI(_data)
    pass


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
        session.commit
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

    @classmethod
    def include_album(cls, trackdata):
        t = trackdata.get('track',{})
        child = t.get('uri', '')
        a = t.get('album', {})
        parent = a.get('uri', '')

        inc = session.merge( Include(parent, child) )
        album = session.query(SpotifyAlbum).filter(
            SpotifyAlbum.uri == parent
        ).first()
        # Retrive from API if not exists
        if not album:
            albumdata = { 'album': cls.API.get_a_album(a.get('id')) }
            album = session.merge( SpotifyAlbum(albumdata) )
            ref = session.merge( Reference(album) )
            print( '\t[  APPENDIX  ] {} [ALBUM].'.format(ref) )
        session.commit()

        return album

    @classmethod
    def include_artists(cls, trackdata):
        t = trackdata.get('track', {})
        child = t.get('uri')

        refs = []
        for r in t.get('artists', []):
            parent = r.get('uri')
            inc = session.merge( Include(parent, child) )
            artist = session.query(SpotifyArtist).filter(
                SpotifyArtist.uri == parent
            ).first()
            # Retrive from API if not exists
            if not artist:
                artistdata = cls.API.get_a_artist( r.get('id') )
                artist = session.merge( SpotifyArtist(artistdata) )
                refs.append( session.merge(Reference(artist)) )
                print( '\t[  APPENDIX  ] {} [ARTISTS].'.format(refs) )
            # break
        session.commit()

        return refs




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

    @classmethod
    def include_tracks(cls, albumdata):
        album = albumdata.get('album', {})
        parent = album.get('uri')
        refs = []
        for page in cls.API.get_album_tracks(album.get('id')):
            for o in page.get('items', []):
                child = o.get('uri')
                if not child: continue
                inc = session.merge( Include(parent, child) )
                trackdata = {'track': o}
                refs.append( SptOpsTrack.load(trackdata) )
                SptOpsTrack.include_artists(trackdata)
            # break
        print( '\t[  APPENDIX  ] {} [TRACKS].'.format(len(refs)) )
        session.commit()

        return refs

    @classmethod
    def include_artists(cls, albumdata):
        album = albumdata.get('album', {})
        child = album.get('uri')
        refs = []
        artists = album.get('artists',[])
        for r in artists:
            parent = r.get('uri')
            inc = session.merge( Include(parent, child) )
            artist = session.query( SpotifyArtist ).filter(
                SpotifyArtist.uri == parent
            ).first()
            # Insert artist data if not exists
            if not artist:
                artistdata = cls.API.get_a_artist( r.get('id') )
                artist = session.merge( SpotifyArtist(artistdata) )
                refs.append( session.merge(Reference(artist)) )
                print( '\t[  APPENDIX  ] {} [ARTISTS].'.format(refs) )
            # break
        session.commit()

        return refs



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

    @classmethod
    def include_tracks(cls, playlistdata):
        parent = playlistdata.get('uri')
        refs = []
        for page in cls.API.get_playlist_tracks(playlistdata.get('id')):
            for o in page.get('items', []):
                child = o.get('track',{}).get('uri')
                if not child: continue
                inc = session.merge( Include(parent, child) )
                refs.append( SptOpsTrack.load(o) )
                # SptOpsTrack.include_album(o)
                # SptOpsTrack.include_artists(o)
            # break
        print( '\t[  APPENDIX  ] {} [TRACKS].'.format(len(refs)) )
        session.commit()

        return refs



