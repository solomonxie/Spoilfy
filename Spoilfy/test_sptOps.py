#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import os
import uuid
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

class TestSptOpsAccount(unittest.TestCase):

    def setUp(self):
        self.Ops = SptOpsAccount()
        with open('../test/data/spotify/user.json', 'r') as f:
            self.jsondata = json.loads( f.read() )

    def test_data(self):
        uri = 'spotify:user:22ctjaxuyoesd3ici65zqcbxa'
        name = 'Solomon Xie'
        self.assertEqual(self.jsondata['uri'], uri)
        self.assertEqual(self.jsondata['display_name'], name)

    def test_insert(self):
        user = self.Ops.insert( self.jsondata )
        self.assertEqual(user.name, 'Solomon Xie')




class TestSptOpsTrack(unittest.TestCase):

    def setUp(self):
        self.Ops = SptOpsTrack()
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

    def test_loads(self):
        ref1, ref2 = self.Ops.loads( self.jsondata )
        self.assertEqual(ref1.uri, 'spotify:track:1WvIkhx5AxsA4N9TgkYSQG')
        self.assertEqual(ref2.uri, 'spotify:track:70bq0ZJVXu93cvGlluYrXu')



class TestSptOpsAlbum(unittest.TestCase):

    def setUp(self):
        self.Ops = SptOpsAlbum()

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

    def test_loads(self):
        ref1, ref2 = self.Ops.loads( self.jsondata )
        self.assertEqual(ref1.uri, 'spotify:album:7GJspOwIWdFfzJfxN8oVTF')
        self.assertEqual(ref2.uri, 'spotify:album:75rqM0qScdcFoP4sprrHJN')



class TestSptOpsArtist(unittest.TestCase):

    def setUp(self):
        self.Ops = SptOpsArtist()
        with open('../test/data/spotify/artists.json', 'r') as f:
            self.jsondata = json.loads( f.read() )
            self.artist1 = self.jsondata['artists']['items'][0]
            self.artist2 = self.jsondata['artists']['items'][1]

    def test_data(self):
        items = self.jsondata['artists']['items']
        self.assertIsInstance( items, list )
        self.assertIsNotNone( items[0].get('followers') )
        self.assertIsNotNone( items[0].get('popularity') )

    def test_loads(self):
        ref1, ref2 = self.Ops.loads( self.jsondata )
        self.assertEqual(ref1.uri, 'spotify:artist:04gDigrS5kc9YWfZHwBETP')
        self.assertEqual(ref2.uri, 'spotify:artist:08WRjJPbPqSEOkFuc99ymW')



class TestSptOpsPlaylist(unittest.TestCase):

    def setUp(self):
        self.Ops = SptOpsPlaylist()
        with open('../test/data/spotify/playlists.json', 'r') as f:
            self.jsondata = json.loads( f.read() )
            self.playlist1 = self.jsondata['items'][0]
            self.playlist2 = self.jsondata['items'][1]

        with open('../test/data/spotify/playlist_tracks.json', 'r') as f:
            self.tracks = json.loads( f.read() )

    def test_data(self):
        items = self.jsondata['items']
        self.assertIsInstance( items, list )
        self.assertIsNotNone( items[0].get('uri') )
        self.assertIsNotNone( items[0].get('owner') )
        tracks = self.tracks['items']
        self.assertIsInstance( tracks, list )
        self.assertIsNotNone( tracks[0].get('track') )
        self.assertIsNotNone( tracks[0].get('track',{}).get('uri') )

    def test_loads(self):
        ref1, ref2 = self.Ops.loads( self.jsondata )
        self.assertEqual(ref1.uri, 'spotify:playlist:6FaSdKCximiMF0wupKF9hW')
        self.assertEqual(ref2.uri, 'spotify:playlist:1bBu4pZv4G7N6aj2vrcwah')





class TestSptOpsMissing(unittest.TestCase):

    def setUp(self):
        # Connect Database
        self.dbpath = '/tmp/{}.sqlite'.format(uuid.uuid1().hex)
        self.engine = create_engine('sqlite:///'.format(self.dbpath), echo=True)
        self.session = sessionmaker(bind=self.engine, autoflush=False)()

    def tearDown(self):
        if os.path.exists(self.dbpath):
            os.remove(self.dbpath)
            prrint('Temp db deleted.')

    def test_find_missing_tracks(self):
        pass



class TestSptOpsInclude(unittest.TestCase):

    def setUp(self):
        self.Ops = SptOpsInclude()
        # Connect Database
        # self.dbpath = 'sqlite:////tmp/{}.sqlite'.format(uuid.uuid1().hex)
        # self.dbpath = 'sqlite:///:memory:'
        self.dbpath = 'sqlite:////tmp/tmpdb.sqlite'
        self.engine = create_engine( self.dbpath )
        self.session = sessionmaker(bind=self.engine, autoflush=False)()
        Base.metadata.create_all(bind=self.engine)

        # Make temporary session for Operators
        self.T = SptOpsTrack(session=self.session)
        self.A = SptOpsAlbum(session=self.session)
        self.R = SptOpsArtist(session=self.session)
        self.P = SptOpsPlaylist(session=self.session)
        self.I = SptOpsInclude(session=self.session)

        # Load sample resources
        with open('../test/data/spotify/tracks.json', 'r') as f:
            self.T.loads( json.loads(f.read()) )
        with open('../test/data/spotify/albums.json', 'r') as f:
            self.A.loads( json.loads(f.read()) )
        with open('../test/data/spotify/artists.json', 'r') as f:
            self.R.loads( json.loads(f.read()) )
        with open('../test/data/spotify/playlists.json', 'r') as f:
            self.P.loads( json.loads(f.read()) )


    def tearDown(self):
        # if os.path.exists(self.dbpath):
            # os.remove(self.dbpath)
            # print('Temp db deleted.')
        # Base.metadata.drop_all( self.engine )
        pass


    def test_find_unbinded(self):
        unbinded = self.Ops.find_unbinded(self.Ops.SQL_TRACK_ALBUMS)
        print('[UNBINDED]', len(unbinded))
        self.assertEqual(1,1)


if __name__ == '__main__':
    # unittest.main(TestSptOpsInclude(), verbosity=2)
    unittest.main(verbosity=2)
