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
    #THIS
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
    # with open('../scratch/sqlschemas/spotify/jsondumps-full/get_user_profile.json', 'r') as f:
        # jsondata = json.loads( f.read() )
    me = SptOpsAccount.get_my_profile()
    print( '\t Me:', me.name )



def test_SptOpsTrack():
    print( '\n[  TEST  ] SptOpsTrack' )
    # Add a track
    # with open('../scratch/sqlschemas/spotify/jsondumps-full/get_user_tracks.json', 'r') as f:
        # jsondata = json.loads( f.read() )
        # tracks = SptOpsTrack.loads( jsondata )
        # print( '[  OK  ] Inserted {} User tracks.'.format(len(tracks)) )
    for page in SptOpsTrack.API.get_my_tracks():
        tracks = SptOpsTrack.loads( page )
        print( '[  OK  ] Inserted {} User tracks.'.format(len(tracks)) )
        break


def test_SptOpsAlbum():
    print( '\n[  TEST  ] SptOpsAlbum' )
    # Add an album
    # with open('../scratch/sqlschemas/spotify/jsondumps-full/get_user_albums.json', 'r') as f:
        # jsondata = json.loads( f.read() )
    for page in SptOpsAlbum.API.get_my_albums():
        albums = SptOpsAlbum.loads( page )
        print( '[  OK  ] Inserted {} User albums.'.format(len(albums)) )
        break



def test_SptOpsArtist():
    print( '\n[  TEST  ] SptOpsArtist' )
    # Add an artist
    # with open('../scratch/sqlschemas/spotify/jsondumps-full/get_user_artists.json', 'r') as f:
        # jsondata = json.loads( f.read() )
    for page in SptOpsArtist.API.get_my_artists():
        artists = SptOpsArtist.loads( page )
        print( '[  OK  ] Inserted {} User artists.'.format(len(artists)) )
        break



def test_SptOpsPlaylist():
    print( '\n[  TEST  ] SptOpsPlaylist' )
    # Add a playlist
    # with open('../scratch/sqlschemas/spotify/jsondumps-full/get_user_playlists.json', 'r') as f:
        # jsondata = json.loads( f.read() )
    for page in SptOpsPlaylist.API.get_my_playlists():
        playlists = SptOpsPlaylist.loads( page )
        print( '[  OK  ] Inserted {} User playlists.'.format(len(playlists)) )
        break




if __name__ == '__main__':
    try:
        # SpotifyAccount.__table__.drop(engine)
        # SpotifyTrack.__table__.drop(engine)
        # SpotifyAlbum.__table__.drop(engine)
        # SpotifyArtist.__table__.drop(engine)
        # SpotifyPlaylist.__table__.drop(engine)
        # Include.__table__.drop(engine)
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


