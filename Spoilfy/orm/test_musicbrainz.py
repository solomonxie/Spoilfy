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
from musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzArtist

session = sessionmaker(bind=engine, autoflush=False)()




# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

def test_MusicbrainzTrack():
    try:
        MusicbrainzTrack.__table__.drop(engine)
        MusicbrainzTrack.metadata.create_all(bind=engine)
    except Exception as e:
        print('Error on dropping Musicbrainz table.')


    # Add a track
    path = '../../scratch/sqlschemas/musicbrainz/jsondumps/search_recording.json'
    with open(path, 'r') as f:
        jsondata = json.loads( f.read() )
        # Create items
        items = MusicbrainzTrack.add_resources(jsondata['recordings'])
        # Make NEW reference
        Reference.add_resources(items)


def test_MusicbrainzAlbum():
    try:
        MusicbrainzAlbum.__table__.drop(engine)
        MusicbrainzAlbum.metadata.create_all(bind=engine)
    except Exception as e:
        print('Error on dropping Musicbrainz table.')


    # Add a track
    path = '../../scratch/sqlschemas/musicbrainz/jsondumps/search_release.json'
    with open(path, 'r') as f:
        jsondata = json.loads( f.read() )
        # Create items
        items = MusicbrainzAlbum.add_resources(jsondata.get('releases',{}))
        # Make NEW reference
        Reference.add_resources(items)


def test_MusicbrainzArtist():
    try:
        MusicbrainzArtist.__table__.drop(engine)
        MusicbrainzArtist.metadata.create_all(bind=engine)
    except Exception as e:
        print('Error on dropping Musicbrainz table.')


    # Add a track
    path = '../../scratch/sqlschemas/musicbrainz/jsondumps/search_artists.json'
    with open(path, 'r') as f:
        jsondata = json.loads( f.read() )
        # Create items
        items = MusicbrainzArtist.add_resources(jsondata.get('artists',{}))
        # Make NEW reference
        Reference.add_resources(items)




def test_query_track():
    pass


def test_query_album():
    pass


def test_query_artist():
    pass




if __name__ == '__main__':
    #=> Insert data
    test_MusicbrainzTrack()
    test_MusicbrainzAlbum()
    test_MusicbrainzArtist()

    #=> Query
    # test_query_track()
    # test_query_album()
    # test_query_artist()

