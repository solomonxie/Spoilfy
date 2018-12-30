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
from spotify import SpotifyAccount, SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist

session = sessionmaker(bind=engine, autoflush=False)()




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
        item = SpotifyAccount(jsondata)
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
    me = UserAccount.query.first()
    print( '[USER]', me.uri )

    # Search all tracks of a user
    query = session.query(
        UserResource, Reference, SpotifyTrack
    ).filter(
        UserResource.owner_uri == me.uri,
        UserResource.type == 'track'
    ).filter(
        Reference.real_uri == UserResource.real_uri
    ).filter(
        SpotifyTrack.uri == Reference.uri
    )
    print( '[SQL]', query )
    results = query.all()
    print( '[RESULTS]', len(results) )
    for rsc, ref, t in results:
        print( '[NAME]', t.name )


def test_query_album():
    # Get a user
    me = UserAccount.query.first()
    print( '[USER]', me.uri )

    # search all albums of a user
    query = session.query(
        UserResource, Reference, SpotifyAlbum
    ).filter(
        UserResource.owner_uri == me.uri,
        UserResource.type == 'album'
    ).filter(
        Reference.real_uri == UserResource.real_uri
    ).filter(
        SpotifyAlbum.uri == Reference.uri
    )
    print( '[SQL]', query )
    results = query.all()
    print( '[RESULTS]', len(results) )
    for rsc, ref, t in results:
        print( '[NAME]', t.name )


def test_query_artist():
    # Get a user
    me = UserAccount.query.first()
    print( '[USER]', me.uri )

    # search all albums of a user
    query = session.query(
        UserResource, Reference, SpotifyArtist
    ).filter(
        UserResource.owner_uri == me.uri,
        UserResource.type == 'artist'
    ).filter(
        Reference.real_uri == UserResource.real_uri
    ).filter(
        SpotifyArtist.uri == Reference.uri
    )
    print( '[SQL]', query )
    results = query.all()
    print( '[RESULTS]', len(results) )
    for rsc, ref, t in results:
        print( '[NAME]', t.name )


def test_query_playlist():
    # Get a user
    me = UserAccount.query.first()
    print( '[USER]', me.uri )

    # search all albums of a user
    query = session.query(
        UserResource, Reference, SpotifyPlaylist
    ).filter(
        UserResource.owner_uri == me.uri,
        UserResource.type == 'playlist'
    ).filter(
        Reference.real_uri == UserResource.real_uri
    ).filter(
        SpotifyPlaylist.uri == Reference.uri
    )
    print( '[SQL]', query )
    results = query.all()
    print( '[RESULTS]', len(results) )
    for rsc, ref, t in results:
        print( '[NAME]', t.name )


if __name__ == '__main__':
    #=> Insert data
    test_SpotifyAccount()
    test_SpotifyTrack()
    test_SpotifyAlbum()
    test_SpotifyArtist()
    test_SpotifyPlaylist()

    #=> Query
    # test_query_track()
    # test_query_album()
    # test_query_artist()
    # test_query_playlist()

