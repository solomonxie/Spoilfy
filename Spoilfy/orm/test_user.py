#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import unittest
import json

from common import Base, engine, session, Resource, Reference
from user import UserAccount, UserResource
from spotify import SpotifyAccount, SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist



# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


class TestUserAccount(unittest.TestCase):

    def test_UserAccount(self):
        # Add a User Account
        with open('./users.json', 'r') as f:
            jsondata = json.loads( f.read() )
            # UserAccount.loads( jsondata )

class TestUserResource(unittest.TestCase):

    def test_UserResource(self):
        # Get a user
        user = UserAccount.query.first()

        # 1.Add User tracks
        items = Reference.query.filter(Reference.type=='track').all()
        # UserResource.add_resources(user.uri, items)
        # 2.Add User albums
        items = Reference.query.filter(Reference.type=='album').all()
        # UserResource.add_resources(user.uri, items)
        # 3.Add User artists
        items = Reference.query.filter(Reference.type=='artist').all()
        # UserResource.add_resources(user.uri, items)
        # 4.Add User playlists
        items = Reference.query.filter(Reference.type=='playlist').all()
        # UserResource.add_resources(user.uri, items)


    def test_UserResource2(self):
        # Get a user
        me = UserAccount.query.first()

        t = '../../test/data/spotify/tracks.json'
        a = '../../test/data/spotify/albums.json'
        r = '../../test/data/spotify/artist.json'
        p = '../../test/data/spotify/playlists.json'

        with open(t, 'r') as f:
            jsondata = json.loads( f.read() )
            # refs = SpotifyTrack.loads( jsondata )
            # me.bind_resources( refs )
        with open(a, 'r') as f:
            jsondata = json.loads( f.read() )
            # refs = SpotifyAlbum.loads( jsondata )
            # me.bind_resources( refs )
        with open(r, 'r') as f:
            jsondata = json.loads( f.read() )
            # refs = SpotifyArtist.loads( jsondata )
            # me.bind_resources( refs )
        with open(p, 'r') as f:
            jsondata = json.loads( f.read() )
            # refs = SpotifyPlaylist.loads( jsondata )
            # me.bind_resources( refs )



if __name__ == '__main__':
    unittest.main()
