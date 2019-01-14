#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json

from sqlalchemy import exists
from sqlalchemy.orm import aliased


#-> TEST only
if __name__ in ['__main__', 'spotify2mbz']:
    from orm.spotify import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist, SpotifyAccount
    from orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    from orm.common import Base, engine, session
    from orm.common import Resource, Reference, Include
    from webapi.apiSpotify import SpotifyAPI
    import webapi.apiMusicbrainz as MbzAPI
else:
    from Spoilfy.orm.spotify import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist, SpotifyAccount
    from Spoilfy.orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    from Spoilfy.orm.common import Base, engine, session
    from Spoilfy.orm.common import Resource, Reference, Include
    from Spoilfy.webapi.apiSpotify import SpotifyAPI
    import Spoilfy.webapi.apiMusicbrainz as MbzAPI


class Mapper:
    """ [ Map Spotify item to Musicbrainz ]

        Steps:
        - Read a spotify item's info
        - Check if related local mbz info exists
        - Request Musicbrainz API for the info
        - Save the best match to Database
    """

    def get_references(self, track_uri):
        print('[NOW]__get_references__')
        query = session.query(Reference).filter(
            Reference.uri == track_uri
        )
        print( '\t[REFs]', query.all() )

        # Spotify
        refs = list(filter(lambda o: o.provider=='spotify', query.all()))
        spt = refs[0] if refs else None
        print( '\t[SPT]', spt )

        # Musicbrainz
        refs = list(filter(lambda o: o.provider=='musicbrainz', query.all()))
        mbz = refs[0] if refs else None
        print( '\t[MBZ]', mbz )

        return mbz, spt

    def get_spotify_info(self, uri):
        print( '[get_spotify_info()] TO BE IMPLEMENTED' )

    def get_musicbrainz_info(self, real_uri, **query):
        print( '[get_musicbrainz_info()] TO BE IMPLEMENTED' )

    @classmethod
    def mapItems(cls, uris):
        for uri in uris:
            tag = cls(uri)



class MapTrack(Mapper):
    """ [ Map a Spotify track to Musicbrainz ]
    """

    def __init__(self, uri):
        """
            Params:
            - uri [type:String]: spotify track's uri
        """
        # Check track's references [Spotify] & [Musicbrainz]
        mbz,spt = self.get_references( uri )

        # Retrive tags from MBZ for this track if not exists
        info = self.get_spotify_info( uri ) if not mbz else None
        if info:
            track, album, artist = info
            print( '\t', track.name, album.name, artist.name )
            # Tagging
            self.tag = mbz = self.get_musicbrainz_info(
                spt.real_uri, track, album, artist
            )
            print( '[TAG]', mbz.name, mbz.uri )

    def get_spotify_info(self, uri):
        print('[NOW]__get_spt_info__:{}'.format(uri))
        # -> Middlewares for Many-to-Many tables
        trackAlbum = aliased(Include)
        trackArtists = aliased(Include)

        # -> Compose SQL
        info = session.query(
            SpotifyTrack, SpotifyAlbum
        ).filter(
            SpotifyTrack.uri == uri,
            SpotifyTrack.uri == trackAlbum.child_uri,
            SpotifyAlbum.uri == trackAlbum.parent_uri
        ).first()
        track, album = info if info else (None, None)
        print( 'track, album:', track, album )

        info = session.query(
            SpotifyArtist
        ).filter(
            SpotifyTrack.uri == uri,
            SpotifyTrack.uri == trackArtists.child_uri,
            SpotifyArtist.uri == trackArtists.parent_uri
        ).first()
        artist = info if info else None
        print( 'artist:', artist )

        print( track, album, artist )
        return (track, album, artist)

    def get_musicbrainz_info(self, real_uri, track, album, artist):
        print('[NOW]__tagging__')
        jsondata = MbzAPI.best_match_track(
            name=track.name, release=album.name, artist=artist.name,
        )
        return MusicbrainzTrack.load( jsondata, real_uri )



class MapAlbum(Mapper):
    """ [ Map a Spotify album to Musicbrainz ]
    """

    def __init__(self, uri):
        """
            Params:
            - uri [type:String]: spotify album's uri
        """
        # Check track's references [Spotify] & [Musicbrainz]
        mbz,spt = self.get_references( uri )

        # Retrive tags from MBZ for this album if not exists
        if not mbz:
            # Get this track's info
            album, artist = self.get_spotify_info( uri )
            print( '\t', album.name, artist.name )
            # Tagging
            self.tag = mbz = self.get_musicbrainz_info(spt.real_uri, album, artist)
            print( '[  TAG  ]', mbz.name, mbz.uri )

    def get_spotify_info(self, uri):
        print('[NOW]__get_spotify_album_info__')
        # -> Middlewares for Many-to-Many tables
        albumArtists = aliased(Include)
        # -> Compose SQL
        query = session.query(
                SpotifyAlbum, SpotifyArtist
                #Debug: SpotifyAlbum.name, SpotifyArtist.name
            ).join(
                albumArtists, SpotifyAlbum.uri == albumArtists.child_uri
            ).filter(
                SpotifyArtist.uri == albumArtists.parent_uri,
                SpotifyAlbum.uri == uri
            )
        # print( query.all().__len__(), query )
        # ->
        return query.first()

    def get_musicbrainz_info(self, real_uri, album, artist):
        print('[NOW]__tagging__')
        jsondata = MbzAPI.best_match_album(
            name=album.name, artist=artist.name,
        )
        mbz = MusicbrainzAlbum.load( jsondata, real_uri )
        return mbz



class MapArtist(Mapper):
    """ [ Map a Spotify artist to Musicbrainz ]
    """

    def __init__(self, uri):
        """
            Params:
            - uri [type:String]: spotify artist's uri
        """
        # Check track's references [Spotify] & [Musicbrainz]
        mbz,spt = self.get_references( uri )

        # Retrive tags from MBZ for this album if not exists
        if not mbz:
            # Get this track's info
            artist = self.get_spotify_info( uri )
            print( '\t', artist.name )
            # Tagging
            self.tag = mbz = self.get_musicbrainz_info(spt.real_uri, artist)
            print( '[  TAG  ]', mbz.name, mbz.uri )

    def get_spotify_info(self, uri):
        print('[NOW]__get_spotify_artist_info__')
        # -> Middlewares for Many-to-Many tables
        albumArtists = aliased(Include)
        # -> Compose SQL
        query = session.query( SpotifyArtist ).filter(
            SpotifyArtist.uri == uri
        )
        # print( query.all().__len__(), query )
        # ->
        return query.first()

    def get_musicbrainz_info(self, real_uri, artist):
        print('[NOW]__tagging__')
        jsondata = MbzAPI.best_match_artist(
            name=artist.name
        )
        print( jsondata )
        mbz = MusicbrainzArtist.load( jsondata, real_uri )
        return mbz



# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


def test_MapTrack():
    # Map a track
    # track_uri = 'spotify:track:0ycrQBLTLJOFLU7SZlNpli'
    # tag = MapTrack(track_uri)

    # Map all existing spotify tracks
    uris = session.query( SpotifyTrack.uri ).all()
    print( len(uris) )
    from time import sleep
    for u, in uris:
        print( u )
        tag = MapTrack(u)
        break
        sleep(2)

    # tags = [ MapTrack(u) for u, in uris]

def test_MapAlbum():
    # Map an album
    album_uri = 'spotify:album:1xn54DMo2qIqBuMqHtUsFd'
    tag = MapAlbum(album_uri)

def test_MapArtist():
    # Map an artist
    artist_uri = 'spotify:artist:04gDigrS5kc9YWfZHwBETP'
    tag = MapArtist(artist_uri)



def main():
    test_MapTrack()
    # test_MapAlbum()
    # test_MapArtist()


if __name__ == '__main__':
    main()





print('[  OK  ] __IMPORTED__: {}'.format(__name__))

