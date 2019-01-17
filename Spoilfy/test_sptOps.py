#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest

from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists


#-------[  Import From Other Modules   ]---------
#-> TEST only
if __name__ in ['__main__']:
    from sptOps import *
    from orm.common import *
    from orm.user import *
    from orm.spotify import *
    from orm.musicbrainz import *
    from webapi.apiSpotify import *
    from webapi.apiMusicbrainz import *
else:
    # Package Import Hint: $ python -m Spoilfy.sptOps
    from Spoilfy.sptOps import *
    from Spoilfy.orm.common import *
    from Spoilfy.orm.user import *
    from Spoilfy.orm.spotify import *
    from Spoilfy.orm.musicbrainz import *
    from Spoilfy.webapi.apiSpotify import *
    from Spoilfy.webapi.apiMusicbrainz import *




# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

class test_SptOpsAccount(unittest.TestCase):

    def setUp(self):
        self.cls = SptOpsAccount

    def test_load(self):
        with open('../test/data/spotify/user.json', 'r') as f:
            jsondata = json.loads( f.read() )

        user = self.cls.load(jsondata)
        self.assertEqual(user.name, 'Solomon Xie')




class test_SptOpsTrack(unittest.TestCase):

    def setUp(self):
        self.cls = SptOpsTrack

    def test_load(self):
        with open('../test/data/spotify/tracks.json', 'r') as f:
            jsondata = json.loads( f.read() )

        ref = self.cls.load(jsondata['items'][0])
        self.assertEqual(ref.uri, 'spotify:track:1WvIkhx5AxsA4N9TgkYSQG')

    def test_include_album(self):
        pass

    def test_include_artists(self):
        pass




class test_SptOpsAlbum(unittest.TestCase):

    def setUp(self):
        self.cls = SptOpsAlbum

    def test_load(self):
        with open('../test/data/spotify/albums.json', 'r') as f:
            jsondata = json.loads( f.read() )

        ref = self.cls.load(jsondata['items'][0])
        self.assertEqual(ref.uri, 'spotify:album:7GJspOwIWdFfzJfxN8oVTF')


    def xtest_SptOpsAlbum():
        for page in SptOpsAlbum.API.get_my_albums():
            albums = SptOpsAlbum.loads( page )



class test_SptOpsArtist(unittest.TestCase):

    def setUp(self):
        self.cls = SptOpsArtist

    def test_load(self):
        with open('../test/data/spotify/artists.json', 'r') as f:
            jsondata = json.loads( f.read() )

        ref = self.cls.load(jsondata['artists']['items'][0])
        self.assertEqual(ref.uri, 'spotify:artist:04gDigrS5kc9YWfZHwBETP')

    def xtest_SptOpsArtist():
        for page in SptOpsArtist.API.get_my_artists():
            artists = SptOpsArtist.loads( page )



class test_SptOpsPlaylist(unittest.TestCase):

    def setUp(self):
        self.cls = SptOpsPlaylist

    def test_load(self):
        with open('../test/data/spotify/playlists.json', 'r') as f:
            jsondata = json.loads( f.read() )

        ref = self.cls.load(jsondata['items'][0])
        self.assertEqual(ref.uri, 'spotify:playlist:6FaSdKCximiMF0wupKF9hW')

    def xtest_SptOpsPlaylist():
        for page in SptOpsPlaylist.API.get_my_playlists():
            playlists = SptOpsPlaylist.loads( page )




if __name__ == '__main__':
    unittest.main()
