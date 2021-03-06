#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest

from orm.common import *
from orm.user import *
from orm.musicbrainz import *

from mbzOps import *


# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


class TestMbzOpsTrack(unittest.TestCase):

    def setUp(self):
        pass

    def test_MbzOpsTrack(self):
        # Add a track
        path = '../test/data/musicbrainz/recordings.json'
        with open(path, 'r') as f:
            jsondata = json.loads(f.read())
            # MbzOpsTrack.loads( jsondata )


class TestMbzOpsAlbum(unittest.TestCase):

    def setUp(self):
        pass

    def test_MbzOpsAlbum(self):
        # Add a track
        path = '../test/data/musicbrainz/releases.json'
        with open(path, 'r') as f:
            jsondata = json.loads(f.read())
            # MbzOpsAlbum.loads( jsondata )


class TestMbzOpsArtist(unittest.TestCase):

    def setUp(self):
        pass

    def test_MbzOpsArtist(self):
        # Add a track
        path = '../test/data/musicbrainz/artists.json'
        with open(path, 'r') as f:
            jsondata = json.loads(f.read())
            # MbzOpsArtist.loads( jsondata )


if __name__ == '__main__':
    unittest.main(verbosity=2)
