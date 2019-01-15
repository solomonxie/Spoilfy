#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest
from time import sleep


if __name__ in ['__main__', 'spotify2mbz']:
    from orm.spotify import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist, SpotifyAccount
    from orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    from orm.common import Base, engine, session
    from orm.common import Resource, Reference, Include
    from webapi.apiSpotify import SpotifyAPI
    import webapi.apiMusicbrainz as MbzAPI
    from spotify2mbz import MapTrack, MapAlbum, MapArtist
else:
    from Spoilfy.orm.spotify import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist, SpotifyAccount
    from Spoilfy.orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    from Spoilfy.orm.common import Base, engine, session
    from Spoilfy.orm.common import Resource, Reference, Include
    from Spoilfy.webapi.apiSpotify import SpotifyAPI
    import Spoilfy.webapi.apiMusicbrainz as MbzAPI
    from Spoilfy.spotify2mbz import MapTrack, MapAlbum, MapArtist



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
    for u, in uris:
        mbz = MapTrack.toMbz(u)
        if mbz:
            print( '\t[TAG]', mbz )

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



