#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest

from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists


#-------[  Import From Other Modules   ]---------
#-> TEST only
if __name__ in ['__main__']:
    #THIS
    from sptOps import SptOpsAccount, SptOpsTrack, SptOpsAlbum, SptOpsArtist, SptOpsPlaylist
    #ORM
    from orm.common import Base, engine, session
    from orm.common import Resource, Reference, Include
    from orm.spotify import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist, SpotifyAccount
    from orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    #API
    from webapi.apiSpotify import SpotifyAPI
    import webapi.apiMusicbrainz as MbzAPI
else:
    # Package Import Hint: $ python -m Spoilfy.orm.spotify
    from Spoilfy.sptOps import SptOpsAccount, SptOpsTrack, SptOpsAlbum, SptOpsArtist, SptOpsPlaylist
    #ORM
    from Spoilfy.orm.spotify import SpotifyTrack, SpotifyAlbum, SpotifyArtist, SpotifyPlaylist, SpotifyAccount
    from Spoilfy.orm.musicbrainz import MusicbrainzTrack, MusicbrainzAlbum, MusicbrainzAlbum, MusicbrainzArtist
    from Spoilfy.orm.common import Base, engine, session
    from Spoilfy.orm.common import Resource, Reference, Include
    #API
    from Spoilfy.webapi.apiSpotify import SpotifyAPI
    import Spoilfy.webapi.apiMusicbrainz as MbzAPI




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
        tracks = SptOpsTrack.loads( jsondata )
        print( '[  OK  ] Inserted {} User tracks.'.format(len(tracks)) )


def test_SptOpsAlbum():
    print( '\n[  TEST  ] SptOpsAlbum' )
    # Add an album
    with open('../scratch/sqlschemas/spotify/jsondumps-full/get_user_albums.json', 'r') as f:
        jsondata = json.loads( f.read() )
        albums = SptOpsAlbum.loads( jsondata )
        print( '[  OK  ] Inserted {} User albums.'.format(len(albums)) )



def test_SptOpsArtist():
    print( '\n[  TEST  ] SptOpsArtist' )
    # Add an artist
    with open('../scratch/sqlschemas/spotify/jsondumps-full/get_user_artists.json', 'r') as f:
        jsondata = json.loads( f.read() )
        artists = SptOpsArtist.loads( jsondata )
        print( '[  OK  ] Inserted {} User artists.'.format(len(artists)) )



def test_SptOpsPlaylist():
    print( '\n[  TEST  ] SptOpsPlaylist' )
    # Add a playlist
    with open('../scratch/sqlschemas/spotify/jsondumps-full/get_user_playlists.json', 'r') as f:
        jsondata = json.loads( f.read() )
        playlists = SptOpsPlaylist.loads( jsondata )
        print( '[  OK  ] Inserted {} User playlists.'.format(len(playlists)) )



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
        SpotifyAccount.__table__.drop(engine)
        SpotifyTrack.__table__.drop(engine)
        SpotifyAlbum.__table__.drop(engine)
        SpotifyArtist.__table__.drop(engine)
        SpotifyPlaylist.__table__.drop(engine)
        Include.__table__.drop(engine)
        pass
    except Exception as e:
        print('Error on dropping SptOps table.')
    finally:
        Base.metadata.create_all(bind=engine)

    #=> Insert data
    test_SptOpsAccount()
    test_SptOpsTrack()
    test_SptOpsAlbum()
    test_SptOpsArtist()
    test_SptOpsPlaylist()

    #=> Query
    # test_query_track()
    # test_query_album()
    # test_query_artist()
    # test_query_playlist()


