#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest

from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists

from common import engine, session, Resource, Reference
from user import UserAccount, UserResource
from spotify import SpotifyAccount, SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist




# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

def test_SpotifyAccount():
    try:
        SpotifyAccount.__table__.drop(engine)
    except Exception as e:
        print('Error on dropping Spotify table.')
    finally:
        SpotifyAccount.metadata.create_all(bind=engine)

    # Add an account
    with open('../../scratch/sqlschemas/spotify/jsondumps-full/get_user_profile.json', 'r') as f:
        jsondata = json.loads( f.read() )
        # Create items
        item = SpotifyAccount(jsondata)
        # Add reference
        session.merge( Reference(item) )
        session.commit



def test_SpotifyTrack():
    try:
        # pass
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
        # Add binded album
        for track in items:
            album = track.album
            has, = session.query(exists().where(
                SpotifyAlbum.uri == album.get('uri')
            )).first()
            if not has:
                # print( album.get('name') )
                ab = session.merge( SpotifyAlbum({'album':album}) )
                print( ab.name, ab.uri )
                session.commit()

    # Get tracks from DB
    #SpotifyTrack.session.query()


def test_SpotifyAlbum():
    try:
        SpotifyAlbum.__table__.drop(engine)
    except Exception as e:
        print('Error on dropping Spotify table.')
    finally:
        SpotifyAlbum.metadata.create_all(bind=engine)

    # Add an album
    with open('../../scratch/sqlschemas/spotify/jsondumps-full/get_user_albums.json', 'r') as f:
        jsondata = json.loads( f.read() )
        # item = jsondata['items'][0]['album']['tracks']['items'][0]
        items = SpotifyAlbum.add_resources(jsondata['items'])
        # Add reference
        Reference.add_resources(items)


def test_SpotifyArtist():
    try:
        SpotifyArtist.__table__.drop(engine)
    except Exception as e:
        print('Error on dropping Spotify table.')
    finally:
        SpotifyArtist.metadata.create_all(bind=engine)

    # Add an artist
    with open('../../scratch/sqlschemas/spotify/jsondumps-full/get_user_artists.json', 'r') as f:
        jsondata = json.loads( f.read() )
        items = SpotifyArtist.add_resources(jsondata['artists']['items'])
        # Add reference
        Reference.add_resources(items)



def test_SpotifyPlaylist():
    try:
        SpotifyPlaylist.__table__.drop(engine)
    except Exception as e:
        print('Error on dropping Spotify table.')
    finally:
        SpotifyPlaylist.metadata.create_all(bind=engine)

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
        SpotifyTrack.name
    ).filter(
        UserResource.owner_uri == me.uri,
        UserResource.type == 'track',
        UserResource.real_uri == Reference.real_uri,
        Reference.uri == SpotifyTrack.uri
    )
    print( '[SQL]', query )
    results = query.all()
    print( '[RESULTS]', len(results) )
    for name in results:
        print( '[NAME]', name )


def test_query_album():
    # Get a user
    me = UserAccount.query.first()
    print( '[USER]', me.uri )

    # search all albums of a user
    query = session.query(
        SpotifyAlbum.name
    ).filter(
        UserResource.owner_uri == me.uri,
        UserResource.type == 'album',
        Reference.real_uri == UserResource.real_uri,
        SpotifyAlbum.uri == Reference.uri
    )
    print( '[SQL]', query )
    results = query.all()
    print( '[RESULTS]', len(results) )
    for name in results:
        print( '[NAME]', name )


def test_query_artist():
    # Get a user
    me = UserAccount.query.first()
    print( '[USER]', me.uri )

    # search all albums of a user
    query = session.query(
        SpotifyArtist.name
    ).filter(
        UserResource.owner_uri == me.uri,
        UserResource.type == 'artist',
        Reference.real_uri == UserResource.real_uri,
        SpotifyArtist.uri == Reference.uri
    )
    print( '[SQL]', query )
    results = query.all()
    print( '[RESULTS]', len(results) )
    for name in results:
        print( '[NAME]', name )


def test_query_playlist():
    # Get a user
    me = UserAccount.query.first()
    print( '[USER]', me.uri )

    # search all albums of a user
    query = session.query(
        SpotifyPlaylist.name
    ).filter(
        UserResource.owner_uri == me.uri,
        UserResource.type == 'playlist',
        Reference.real_uri == UserResource.real_uri,
        SpotifyPlaylist.uri == Reference.uri
    )
    print( '[SQL]', query )
    results = query.all()
    print( '[RESULTS]', len(results) )
    for name in results:
        print( '[NAME]', name )


if __name__ == '__main__':
    #=> Insert data
    test_SpotifyAccount()
    test_SpotifyTrack()
    test_SpotifyAlbum()
    test_SpotifyArtist()
    test_SpotifyPlaylist()

    #=> Query
    test_query_track()
    test_query_album()
    test_query_artist()
    test_query_playlist()

