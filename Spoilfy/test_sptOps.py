#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest

from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists

from common import engine, Base, session, Resource, Reference, Include
from user import UserAccount, UserResource
from sptOps import SptOpsAccount, SptOpsTrack, SptOpsAlbum, SptOpsArtist, SptOpsPlaylist




# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

def test_SptOpsAccount():
    print( '\n[  TEST  ] SptOpsAccount' )
    # Add an account
    with open('../scratch/sqlschemas/spotify/jsondumps-full/get_user_profile.json', 'r') as f:
        jsondata = json.loads( f.read() )
        SptOpsAccount.load( jsondata )



def test_SptOpsTrack():
    print( '\n[  TEST  ] SptOpsTrack' )
    # Add a track
    with open('../scratch/sqlschemas/spotify/jsondumps-full/get_user_tracks.json', 'r') as f:
        jsondata = json.loads( f.read() )
        SptOpsTrack.loads( jsondata )


def test_SptOpsAlbum():
    print( '\n[  TEST  ] SptOpsAlbum' )
    # Add an album
    with open('../scratch/sqlschemas/spotify/jsondumps-full/get_user_albums.json', 'r') as f:
        jsondata = json.loads( f.read() )
        SptOpsAlbum.loads( jsondata )



def test_SptOpsArtist():
    print( '\n[  TEST  ] SptOpsArtist' )
    # Add an artist
    with open('../scratch/sqlschemas/spotify/jsondumps-full/get_user_artists.json', 'r') as f:
        jsondata = json.loads( f.read() )
        SptOpsArtist.loads( jsondata )



def test_SptOpsPlaylist():
    print( '\n[  TEST  ] SptOpsPlaylist' )
    # Add a playlist
    with open('../scratch/sqlschemas/spotify/jsondumps-full/get_user_playlists.json', 'r') as f:
        jsondata = json.loads( f.read() )
        SptOpsPlaylist.loads( jsondata )



def test_query_track():
    print( '\n[  TEST  ] Query Track' )
    # print( SptOpsTrack.query.all() )

    # Get a user
    me = UserAccount.query.first()
    print( '[USER]', me.uri )

    # Search all tracks of a user
    query = session.query(
        SptOpsTrack.name
    ).filter(
        UserResource.owner_uri == me.uri,
        UserResource.type == 'track',
        UserResource.real_uri == Reference.real_uri,
        Reference.uri == SptOpsTrack.uri
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
        SptOpsAlbum.name
    ).filter(
        UserResource.owner_uri == me.uri,
        UserResource.type == 'album',
        Reference.real_uri == UserResource.real_uri,
        SptOpsAlbum.uri == Reference.uri
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
        SptOpsArtist.name
    ).filter(
        UserResource.owner_uri == me.uri,
        UserResource.type == 'artist',
        Reference.real_uri == UserResource.real_uri,
        SptOpsArtist.uri == Reference.uri
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
        SptOpsPlaylist.name
    ).filter(
        UserResource.owner_uri == me.uri,
        UserResource.type == 'playlist',
        Reference.real_uri == UserResource.real_uri,
        SptOpsPlaylist.uri == Reference.uri
    )
    print( '\t[SQL]', query )
    results = query.all()
    print( '[RESULTS]', len(results) )
    for name in results:
        print( '[NAME]', name )


if __name__ == '__main__':
    try:
        SptOpsAccount.__table__.drop(engine)
        SptOpsTrack.__table__.drop(engine)
        SptOpsAlbum.__table__.drop(engine)
        SptOpsArtist.__table__.drop(engine)
        SptOpsPlaylist.__table__.drop(engine)
        Include.__table__.drop(engine)
        pass
    except Exception as e:
        print('Error on dropping SptOps table.')
    finally:
        Base.metadata.create_all(bind=engine)

    #=> Insert data
    test_SptOpsTrack()
    test_SptOpsAlbum()
    test_SptOpsArtist()
    test_SptOpsPlaylist()
    test_SptOpsAccount()

    #=> Query
    # test_query_track()
    # test_query_album()
    # test_query_artist()
    # test_query_playlist()


