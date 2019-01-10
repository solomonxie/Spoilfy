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
    except Exception as e:
        print('Error on dropping Musicbrainz table.')
    finally:
        MusicbrainzTrack.metadata.create_all(bind=engine)

    # Add a track
    path = '../../scratch/sqlschemas/musicbrainz/jsondumps/search_recording.json'
    with open(path, 'r') as f:
        jsondata = json.loads( f.read() )
        # Create items
        items = MusicbrainzTrack.add_resources(jsondata['recordings'])
        # Add NEW NEW NEW reference
        Reference.add_resources(items)
        # Bind each track's [albums] & [artists]
        for track in jsondata['recordings']:
            MusicbrainzTrack.include_albums( track )
            # MusicbrainzTrack.include_artists( track )


def test_MusicbrainzAlbum():
    try:
        MusicbrainzAlbum.__table__.drop(engine)
    except Exception as e:
        print('Error on dropping Musicbrainz table.')
    finally:
        MusicbrainzAlbum.metadata.create_all(bind=engine)

    # Add a track
    path = '../../scratch/sqlschemas/musicbrainz/jsondumps/search_release.json'
    with open(path, 'r') as f:
        jsondata = json.loads( f.read() )
        # Create items
        items = MusicbrainzAlbum.add_resources(jsondata.get('releases',{}))
        # Make NEW NEW NEW reference
        Reference.add_resources(items)
        # Bind each album's [artists] & [tracks]
        for album in jsondata['recordings']:
            MusicBrainzAlbum.include_artists( album )


def test_MusicbrainzArtist():
    try:
        MusicbrainzArtist.__table__.drop(engine)
    except Exception as e:
        print('Error on dropping Musicbrainz table.')
    finally:
        MusicbrainzArtist.metadata.create_all(bind=engine)


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
    # test_MusicbrainzAlbum()
    # test_MusicbrainzArtist()

    #=> Query
    # test_query_track()
    # test_query_album()
    # test_query_artist()

