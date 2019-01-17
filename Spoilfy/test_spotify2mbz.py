#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest
from time import sleep


if __name__ in ['__main__', 'spotify2mbz']:
    from orm.spotify import *
    from orm.musicbrainz import *
    from orm.common import *
    from webapi.apiSpotify import SpotifyAPI
    import webapi.apiMusicbrainz as MbzAPI
    from spotify2mbz import *
else:
    from Spoilfy.orm.spotify import *
    from Spoilfy.orm.musicbrainz import *
    from Spoilfy.orm.common import*
    from Spoilfy.webapi.apiSpotify import SpotifyAPI
    import Spoilfy.webapi.apiMusicbrainz as MbzAPI
    from Spoilfy.spotify2mbz import *




# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


def test_MapTrack():
    # Map a track
    # track_uri = 'spotify:track:0ycrQBLTLJOFLU7SZlNpli'
    # tag = MapTrack.toMbz(track_uri)
    pass



def test_MapAlbum():
    # Map an album
    album_uri = 'spotify:album:1xn54DMo2qIqBuMqHtUsFd'
    tag = MapAlbum(album_uri)

def test_MapArtist():
    # Map an artist
    artist_uri = 'spotify:artist:04gDigrS5kc9YWfZHwBETP'
    tag = MapArtist(artist_uri)



def main():
    # test_MapTrack()
    # test_MapAlbum()
    # test_MapArtist()


    # Find Unmapped
    # uris = UnMapped.find_unmapped_tracks()
    # print( '[UNMAPPED] {} TRACKS.'.format(len(uris)) )
    # uris = UnMapped.find_unmapped_albums()
    # print( '[UNMAPPED] {} ALBUMS.'.format(len(uris)) )
    # print( uris )
    # uris = UnMapped.find_unmapped_artists()
    # print( '[UNMAPPED] {} ARTISTS.'.format(len(uris)) )

    # Get track query info
    # info = MapTrack.get_spotify_info('spotify:track:035szXq0XeLeFng7v02xaf')
    # print( '[QUERY]', info )

    # Tagging
    # MapTrack.toMbz('spotify:track:035szXq0XeLeFng7v02xaf')
    info = MapAlbum.get_spotify_info('spotify:album:08xX1j4J9RAjjFLwv9S0OD')
    print( info )

    # Multiple Tagging
    # MapTrack.map_all()
    # MapAlbum.map_all()




if __name__ == '__main__':
    main()



