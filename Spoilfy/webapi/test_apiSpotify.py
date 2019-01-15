#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest

from apiSpotify import SpotifyAPI






# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

# Get auth info
with open('./.spotify_app.json', 'r') as f:
    data = json.loads( f.read() )

api = SpotifyAPI(data)


def main():
    # # Get a track
    # print('[FETCHING] a track...')
    # print( '\t', api.get_a_track('4Uyn4iboGtdgqXXSyErTyO').get('name') )
    # # Get an album
    # print('[FETCHING] an album...')
    # print( '\t', api.get_a_album('2Y9IRtehByVkegoD7TcLfi').get('name') )
    # # Get an artist
    # print('[FETCHING] an artist...')
    # print( '\t', api.get_a_artist('0L8ExT028jH3ddEcZwqJJ5').get('name') )
    # # Get a playlist
    # print('[FETCHING] a playlist...')
    # print( '\t', api.get_a_playlist('1N0IfF495qdmrcRB8kAXrf').get('name') )


    # # Get album tracks
    # print('[FETCHING] album tracks...')
    # for page in api.get_album_tracks('2Y9IRtehByVkegoD7TcLfi'):
        # tracks = [ o['name'] for o in page['items'] ]
        # print( '\t', len(tracks), 'tracks' )
    # # Get playlist tracks
    # print('[FETCHING] playlist tracks...')
    # for page in api.get_playlist_tracks('1N0IfF495qdmrcRB8kAXrf'):
        # tracks = [ o['track']['name'] for o in page['items'] ]
        # print( '\t', len(tracks), 'tracks' )


    # Fetch my profile
    print('[FETCHING] Profile...')
    print( api.get_my_profile()['display_name'] )

    # Fetch my tracks
    print('[FETCHING] Tracks...')
    for t in api.get_my_tracks():
        print('At {} / {}, {} per page, Next URL: {}'.format(
            t.get('offset'), t.get('total'), t.get('limit'), t.get('next')
        ))
    # Fetch my albums
    print('[FETCHING] Albums...')
    for t in api.get_my_albums():
        print('At {} / {}, {} per page, Next URL: {}'.format(
            t.get('offset'), t.get('total'), t.get('limit'), t.get('next')
        ))
    # Fetch my artists
    print('[FETCHING] Artists...')
    for t in api.get_my_artists():
        # Artist list DOESN'T support [limit], [offset]
        print('Total {}, Next URL: {}'.format(
            t.get('total'), t.get('next')
        ))

if __name__ == '__main__':
    main()
