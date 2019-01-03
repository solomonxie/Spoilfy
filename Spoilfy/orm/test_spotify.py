#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest

from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists

from common import engine, Base, session, Resource, Reference
from user import UserAccount, UserResource
from spotify import SpotifyAccount, SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist
from spotify import bind_tracks, bind_album, bind_artists




# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

def test_SpotifyAccount():
    print( '\n[  TEST  ] SpotifyAccount' )
    # Add an account
    with open('../../scratch/sqlschemas/spotify/jsondumps-full/get_user_profile.json', 'r') as f:
        jsondata = json.loads( f.read() )
        # Create items
        item = SpotifyAccount(jsondata)
        # Add reference
        session.merge( Reference(item) )
        session.commit



def test_SpotifyTrack():
    print( '\n[  TEST  ] SpotifyTrack' )
    # Add a track
    with open('../../scratch/sqlschemas/spotify/jsondumps-full/get_user_tracks.json', 'r') as f:
        jsondata = json.loads( f.read() )
        # Create items
        items = SpotifyTrack.add_resources(jsondata['items'])
        # Add reference
        Reference.add_resources(items)
        # Bind relationships
        for track in jsondata['items']:
            t = track.get('track',{})
            # Bind album
            bind_album(t.get('uri'), t.get('album',{}))
            # Bind artists
            # SpotifyTrack.bind_artists(track)
            bind_artists(t.get('uri'), t.get('artists',[]))

def test_SpotifyAlbum():
    print( '\n[  TEST  ] SpotifyAlbum' )
    # Add an album
    with open('../../scratch/sqlschemas/spotify/jsondumps-full/get_user_albums.json', 'r') as f:
        jsondata = json.loads( f.read() )
        # item = jsondata['items'][0]['album']['tracks']['items'][0]
        items = SpotifyAlbum.add_resources(jsondata['items'])
        # Add reference
        Reference.add_resources(items)
        # Bind relationships
        for album in jsondata['items']:
            b = album.get('album',{})
            # Bind tracks
            bind_tracks(b.get('uri'), b.get('tracks',{}).get('items',[]))
            # Bind artists
            bind_artists(b.get('uri'), b.get('artists',[]))



def test_SpotifyArtist():
    print( '\n[  TEST  ] SpotifyArtist' )
    # Add an artist
    with open('../../scratch/sqlschemas/spotify/jsondumps-full/get_user_artists.json', 'r') as f:
        jsondata = json.loads( f.read() )
        items = SpotifyArtist.add_resources(jsondata['artists']['items'])
        # Add reference
        Reference.add_resources(items)



def test_SpotifyPlaylist():
    print( '\n[  TEST  ] SpotifyPlaylist' )
    # Add a playlist
    with open('../../scratch/sqlschemas/spotify/jsondumps-full/get_user_playlists.json', 'r') as f:
        jsondata = json.loads( f.read() )
        items = SpotifyPlaylist.add_resources(jsondata['items'])
        # Add reference
        Reference.add_resources(items)



def test_query_track():
    print( '\n[  TEST  ] Query Track' )
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
    print( '\t[SQL]', query )
    results = query.all()
    print( '[RESULTS]', len(results) )
    for name in results:
        print( '[NAME]', name )


def test_query_album():
    print( '\n[  TEST  ] Query Album' )
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
    print( '\t[SQL]', query )
    results = query.all()
    print( '[RESULTS]', len(results) )
    for name in results:
        print( '[NAME]', name )


def test_query_artist():
    print( '\n[  TEST  ] Query Artist' )
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
    print( '\t[SQL]', query )
    results = query.all()
    print( '[RESULTS]', len(results) )
    for name in results:
        print( '[NAME]', name )


def test_query_playlist():
    print( '\n[  TEST  ] Query Playlist' )
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
    print( '\t[SQL]', query )
    results = query.all()
    print( '[RESULTS]', len(results) )
    for name in results:
        print( '[NAME]', name )


if __name__ == '__main__':
    try:
        SpotifyAccount.__table__.drop(engine)
        SpotifyTrack.__table__.drop(engine)
        SpotifyAlbum.__table__.drop(engine)
        SpotifyArtist.__table__.drop(engine)
        SpotifyPlaylist.__table__.drop(engine)
    except Exception as e:
        print('Error on dropping Spotify table.')
    finally:
        Base.metadata.create_all(bind=engine)

    #=> Insert data
    test_SpotifyTrack()
    test_SpotifyAlbum()
    # test_SpotifyArtist()
    # test_SpotifyPlaylist()
    # test_SpotifyAccount()

    #=> Query
    # test_query_track()
    # test_query_album()
    # test_query_artist()
    # test_query_playlist()

