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


class TestUnMapped(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_find_unmapped_tracks(self):
        # Find Unmapped
        # uris = UnMapped.find_unmapped_tracks()
        pass

    def find_unmapped_albums(self):
        # print( '[UNMAPPED] {} TRACKS.'.format(len(uris)) )
        # uris = UnMapped.find_unmapped_albums()
        pass

    def find_unmapped_artists(self):
        # print( '[UNMAPPED] {} ALBUMS.'.format(len(uris)) )
        # print( uris )
        pass

    def find_unmapped_artists(self):
        # uris = UnMapped.find_unmapped_artists()
        # print( '[UNMAPPED] {} ARTISTS.'.format(len(uris)) )
        pass




class TestMapTrack(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_spotify_info(self):
        # uri = 'spotify:track:035szXq0XeLeFng7v02xaf'
        # info = MapTrack.get_spotify_info(uri)
        pass

    def test_tagging(self):
        pass

    def test_map_all(self):
        # MapTrack.map_all()
        pass

    def test_toMbz(self):
        # Map a track
        # track_uri = 'spotify:track:0ycrQBLTLJOFLU7SZlNpli'
        # tag = MapTrack.toMbz(track_uri)
        # mbz = MapTrack.toMbz('spotify:track:035szXq0XeLeFng7v02xaf')
        pass


class TestMapAlbum(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_spotify_info(self):
        pass

    def test_tagging(self):
        pass

    def test_map_all(self):
        # MapAlbum.map_all()
        pass

    def test_toMbz(self):
        # Map an album
        # album_uri = 'spotify:album:1xn54DMo2qIqBuMqHtUsFd'
        # tag = MapAlbum(album_uri)
        # mbz = MapAlbum.toMbz('spotify:album:08xX1j4J9RAjjFLwv9S0OD')
        pass



class TestMapArtist(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_spotify_info(self):
        pass

    def test_tagging(self):
        pass






if __name__ == '__main__':
    unittest.main()



