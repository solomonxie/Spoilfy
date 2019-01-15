#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest

from mbzOps import MbzOpsTrack, MbzOpsAlbum, MbzOpsArtist
from orm.common import Base, engine, session, Resource, Reference, Include
from orm.user import UserAccount, UserResource
from orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzArtist




# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

def test_MbzOpsTrack():
    # Add a track
    path = '../scratch/sqlschemas/musicbrainz/jsondumps/search_recording.json'
    with open(path, 'r') as f:
        jsondata = json.loads( f.read() )
        MbzOpsTrack.loads( jsondata )


def test_MbzOpsAlbum():
    # Add a track
    path = '../scratch/sqlschemas/musicbrainz/jsondumps/search_release.json'
    with open(path, 'r') as f:
        jsondata = json.loads( f.read() )
        MbzOpsAlbum.loads( jsondata )


def test_MbzOpsArtist():
    # Add a track
    path = '../scratch/sqlschemas/musicbrainz/jsondumps/search_artists.json'
    with open(path, 'r') as f:
        jsondata = json.loads( f.read() )
        MbzOpsArtist.loads( jsondata )




if __name__ == '__main__':
    try:
        # MusicbrainzTrack.__table__.drop(engine)
        # MusicbrainzAlbum.__table__.drop(engine)
        # MusicbrainzArtist.__table__.drop(engine)
        # Include.__table__.drop(engine)
        pass
    except Exception as e:
        print('Error on dropping Musicbrainz table.')
    finally:
        Base.metadata.create_all(bind=engine)


    #=> Insert data
    test_MbzOpsTrack()
    test_MbzOpsAlbum()
    test_MbzOpsArtist()
