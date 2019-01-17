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
        with open('../test/data/spotify/user.json', 'r') as f:
            self.jsondata = json.loads( f.read() )

    def test_data(self):
        uri = 'spotify:user:22ctjaxuyoesd3ici65zqcbxa'
        name = 'Solomon Xie'
        self.assertEqual(self.jsondata['uri'], uri)
        self.assertEqual(self.jsondata['display_name'], name)

    def test_load(self):
        user = self.cls.load( self.jsondata )
        self.assertEqual(user.name, 'Solomon Xie')




class test_SptOpsTrack(unittest.TestCase):

    def setUp(self):
        self.cls = SptOpsTrack
        with open('../test/data/spotify/tracks.json', 'r') as f:
            self.jsondata = json.loads( f.read() )
            self.track1 = self.jsondata['items'][0]
            self.track2 = self.jsondata['items'][1]

    def test_data(self):
        items = self.jsondata['items']
        self.assertIsInstance(items, list)
        self.assertIsNotNone( items[0].get('track') )
        self.assertIsNotNone( items[0].get('track').get('album') )
        self.assertIsNotNone( items[0].get('track').get('artists') )

    def test_load(self):
        ref = self.cls.load( self.track1 )
        self.assertEqual(ref.uri, 'spotify:track:1WvIkhx5AxsA4N9TgkYSQG')
        ref = self.cls.load( self.track2 )
        self.assertEqual(ref.uri, 'spotify:track:70bq0ZJVXu93cvGlluYrXu')

    def test_include_album(self):
        inc = self.cls.include_album( self.track1['track'] )
        parent = 'spotify:album:4VsIC2EXBQWIs3jfc2va1f'
        child = 'spotify:track:1WvIkhx5AxsA4N9TgkYSQG'
        self.assertEqual(inc.parent_uri, parent)
        self.assertEqual(inc.child_uri, child)
        # Also search from DB
        inc = session.query(Include).filter(
            Include.parent_uri == parent,
            Include.child_uri == child
        ).first()
        self.assertIsNotNone(inc)

    def test_include_artists(self):
        incs = self.cls.include_artists( self.track1['track'] )
        parent = 'spotify:artist:05MlomiA9La0OiNIAGqECk'
        child = 'spotify:track:1WvIkhx5AxsA4N9TgkYSQG'
        self.assertEqual(incs[0].parent_uri, parent)
        self.assertEqual(incs[0].child_uri, child)
        # Also search from DB
        inc = session.query(Include).filter(
            Include.parent_uri == parent,
            Include.child_uri == child
        ).first()
        self.assertIsNotNone(inc)




class test_SptOpsAlbum(unittest.TestCase):

    def setUp(self):
        self.cls = SptOpsAlbum

        with open('../test/data/spotify/albums.json', 'r') as f:
            self.jsondata = json.loads( f.read() )
            self.album1 = self.jsondata['items'][0]
            self.album2 = self.jsondata['items'][1]

        with open('../test/data/spotify/album_tracks.json', 'r') as f:
            self.albumtracks = json.loads( f.read() )

    def test_data(self):
        items = self.jsondata['items']
        self.assertIsInstance(items, list)
        self.assertIsNotNone( items[0].get('album') )
        self.assertIsNotNone( items[0].get('album').get('tracks') )
        tracks = self.albumtracks['items']
        self.assertIsInstance(tracks, list)
        self.assertIsInstance(tracks[0]['artists'], list)
        self.assertIsNotNone( tracks[0].get('name') )

    def test_load(self):
        ref = self.cls.load( self.album1 )
        self.assertEqual(ref.uri, 'spotify:album:7GJspOwIWdFfzJfxN8oVTF')
        ref = self.cls.load( self.album2 )
        self.assertEqual(ref.uri, 'spotify:album:75rqM0qScdcFoP4sprrHJN')

    def test_include_tracks(self):
        parent = 'spotify:album:1Li4rADxSxjT2g4xqUcMYh'
        child = 'spotify:track:3I1JTx525DKElzlTYOBfZN'
        incs = self.cls.include_tracks( parent, self.albumtracks )
        self.assertEqual(incs[0].parent_uri, parent)
        self.assertEqual(incs[0].child_uri, child)
        # Also search from DB
        inc = session.query(Include).filter(
            Include.parent_uri == parent,
            Include.child_uri == child
        ).first()
        self.assertIsNotNone(inc)

    def test_incldue_artists(self):
        incs = self.cls.include_artists( self.album1['album'] )
        parent = 'spotify:artist:3B9O5mYYw89fFXkwKh7jCS'
        child = 'spotify:album:7GJspOwIWdFfzJfxN8oVTF'
        self.assertEqual(incs[0].parent_uri, parent)
        self.assertEqual(incs[0].child_uri, child)
        # Also search from DB
        inc = session.query(Include).filter(
            Include.parent_uri == parent,
            Include.child_uri == child
        ).first()
        self.assertIsNotNone(inc)



class test_SptOpsArtist(unittest.TestCase):

    def setUp(self):
        self.cls = SptOpsArtist
        with open('../test/data/spotify/artists.json', 'r') as f:
            self.jsondata = json.loads( f.read() )
            self.artist1 = self.jsondata['artists']['items'][0]
            self.artist2 = self.jsondata['artists']['items'][1]

    def test_data(self):
        items = self.jsondata['artists']['items']
        self.assertIsInstance( items, list )
        self.assertIsNotNone( items[0].get('followers') )
        self.assertIsNotNone( items[0].get('popularity') )

    def test_load(self):
        ref = self.cls.load( self.artist1 )
        self.assertEqual(ref.uri, 'spotify:artist:04gDigrS5kc9YWfZHwBETP')
        ref = self.cls.load( self.artist2 )
        self.assertEqual(ref.uri, 'spotify:artist:08WRjJPbPqSEOkFuc99ymW')



class test_SptOpsPlaylist(unittest.TestCase):

    def setUp(self):
        self.cls = SptOpsPlaylist
        with open('../test/data/spotify/playlists.json', 'r') as f:
            self.jsondata = json.loads( f.read() )
            self.playlist1 = self.jsondata['items'][0]
            self.playlist2 = self.jsondata['items'][1]

    def test_data(self):
        items = self.jsondata['items']
        self.assertIsInstance( items, list )
        self.assertIsNotNone( items[0].get('uri') )
        self.assertIsNotNone( items[0].get('owner') )

    def test_load(self):
        ref = self.cls.load( self.playlist1 )
        self.assertEqual(ref.uri, 'spotify:playlist:6FaSdKCximiMF0wupKF9hW')
        ref = self.cls.load( self.playlist2 )
        self.assertEqual(ref.uri, 'spotify:playlist:1bBu4pZv4G7N6aj2vrcwah')




if __name__ == '__main__':
    unittest.main()
