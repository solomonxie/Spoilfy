#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest

from sqlalchemy.orm import sessionmaker

from common import Base, engine, session, Resource, Reference, Include
from user import UserAccount, UserResource
from musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzArtist




# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

def test_MusicbrainzTrack():
    # Add a track
    path = '../../scratch/sqlschemas/musicbrainz/jsondumps/search_recording.json'
    with open(path, 'r') as f:
        jsondata = json.loads( f.read() )
        MusicbrainzTrack.loads( jsondata )


def test_MusicbrainzAlbum():
    # Add a track
    path = '../../scratch/sqlschemas/musicbrainz/jsondumps/search_release.json'
    with open(path, 'r') as f:
        jsondata = json.loads( f.read() )
        MusicbrainzAlbum.loads( jsondata )


def test_MusicbrainzArtist():
    # Add a track
    path = '../../scratch/sqlschemas/musicbrainz/jsondumps/search_artists.json'
    with open(path, 'r') as f:
        jsondata = json.loads( f.read() )
        MusicbrainzArtist.loads( jsondata )




def test_query_track():
    pass


def test_query_album():
    pass


def test_query_artist():
    pass




if __name__ == '__main__':
    try:
        MusicbrainzTrack.__table__.drop(engine)
        MusicbrainzAlbum.__table__.drop(engine)
        MusicbrainzArtist.__table__.drop(engine)
        # Include.__table__.drop(engine)
    except Exception as e:
        print('Error on dropping Musicbrainz table.')
    finally:
        Base.metadata.create_all(bind=engine)


    #=> Insert data
    test_MusicbrainzTrack()
    test_MusicbrainzAlbum()
    test_MusicbrainzArtist()

    #=> Query
    # test_query_track()
    # test_query_album()
    # test_query_artist()

