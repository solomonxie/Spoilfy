#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import unittest
import json

from common import engine, Resource, Reference
from spotify import SpotifyAccount, SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist
from user import UserAccount, UserResource




# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

def test_SpotifyAccount():
    try:
        SpotifyAccount.__table__.drop(engine)
        SpotifyAccount.metadata.create_all(bind=engine)
    except Exception as e:
        print('Error on dropping Spotify table.')

    # Add an account
    with open('../../scratch/sqlschemas/spotify/jsondumps-full/get_user_profile.json', 'r') as f:
        jsondata = json.loads( f.read() )
        # Create items
        item = SpotifyAccount.add(jsondata)
        # Add reference
        Reference.add(item)



def test_SpotifyTrack():
    try:
        SpotifyTrack.__table__.drop(engine)
        SpotifyTrack.metadata.create_all(bind=engine)
    except Exception as e:
        print('Error on dropping Spotify table.')

    # Add a track
    with open('../../scratch/sqlschemas/spotify/jsondumps-full/get_user_tracks.json', 'r') as f:
        jsondata = json.loads( f.read() )
        # Create items
        items = SpotifyTrack.add_resources(jsondata['items'])
        # Add reference
        Reference.add_resources(items)

    # Get tracks from DB
    #SpotifyTrack.session.query()


def test_SpotifyAlbum():
    try:
        SpotifyAlbum.__table__.drop(engine)
        SpotifyAlbum.metadata.create_all(bind=engine)
    except Exception as e:
        print('Error on dropping Spotify table.')

    # Add an album
    with open('../../scratch/sqlschemas/spotify/jsondumps-full/get_user_albums.json', 'r') as f:
        jsondata = json.loads( f.read() )
        items = SpotifyAlbum.add_resources(jsondata['items'])
        # Add reference
        Reference.add_resources(items)


def test_SpotifyArtist():
    try:
        SpotifyArtist.__table__.drop(engine)
        SpotifyArtist.metadata.create_all(bind=engine)
    except Exception as e:
        print('Error on dropping Spotify table.')

    # Add an artist
    with open('../../scratch/sqlschemas/spotify/jsondumps-full/get_user_artists.json', 'r') as f:
        jsondata = json.loads( f.read() )
        items = SpotifyArtist.add_resources(jsondata['artists']['items'])
        # Add reference
        Reference.add_resources(items)



def test_SpotifyPlaylist():
    try:
        SpotifyPlaylist.__table__.drop(engine)
        SpotifyPlaylist.metadata.create_all(bind=engine)
    except Exception as e:
        print('Error on dropping Spotify table.')

    # Add a playlist
    with open('../../scratch/sqlschemas/spotify/jsondumps-full/get_user_playlists.json', 'r') as f:
        jsondata = json.loads( f.read() )
        items = SpotifyPlaylist.add_resources(jsondata['items'])
        # Add reference
        Reference.add_resources(items)



def test_query_track():
    # print( SpotifyTrack.query.all() )

    # Get a user
    user = UserAccount.query.first()
    print( '[USER]', user.uri )
    # Get all spotify tracks of a user
    tracks = UserResource.query.filter(
        UserResource.uri == user.uri
    ).filter(
        Reference.type == 'track'
    ).all()
    print( tracks )




if __name__ == '__main__':
    # test_SpotifyAccount()
    # test_SpotifyTrack()
    # test_SpotifyAlbum()
    # test_SpotifyArtist()
    # test_SpotifyPlaylist()
    test_query_track()

