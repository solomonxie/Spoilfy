#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest

from sqlalchemy.orm import sessionmaker

from common import engine, Resource, Reference
from user import UserAccount, UserResource
from musicbrainz import MusicbrainzAccount, MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzArtist, MusicbrainzPlaylist

session = sessionmaker(bind=engine, autoflush=False)()




# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

def test_MusicbrainzAccount():
    pass


def test_MusicbrainzTrack():
    pass


def test_MusicbrainzAlbum():
    pass


def test_MusicbrainzArtist():
    pass


def test_MusicbrainzPlaylist():
    pass


def test_query_track():
    pass


def test_query_album():
    pass


def test_query_artist():
    pass


def test_query_playlist():
    pass



if __name__ == '__main__':
    #=> Insert data
    test_MusicbrainzAccount()
    test_MusicbrainzTrack()
    test_MusicbrainzAlbum()
    test_MusicbrainzArtist()
    test_MusicbrainzPlaylist()

    #=> Query
    test_query_track()
    test_query_album()
    test_query_artist()
    test_query_playlist()

