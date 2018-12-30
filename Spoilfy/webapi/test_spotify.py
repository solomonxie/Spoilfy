#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest

from spotify import SpotifyAPI






# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

def main():
    # Get auth info
    with open('./.spotify_app.json', 'r') as f:
        data = json.loads( f.read() )

    api = SpotifyAPI(data)
    # Fetch my profile
    print('[FETCHING] Profile...')
    print( api.get_my_profile()['display_name'] )

    # Fetch my tracks
    print('[FETCHING] Tracks...')
    for t in api.get_my_tracks():
        print('At {} / {}, {} per page, Next URL: \n\t{}'.format(
            t['offset'], t['total'], t['limit'], t['next']
        ))
    # Fetch my albums
    print('[FETCHING] Albums...')
    for t in api.get_my_albums():
        print('At {} / {}, {} per page, Next URL: \n\t{}'.format(
            t['offset'], t['total'], t['limit'], t['next']
        ))
    # Fetch my artists
    print('[FETCHING] Artists...')
    for t in api.get_my_artists():
        # Artist list DOESN'T support [limit], [offset]
        print('Total {}, Next URL: \n\t{}'.format(
            t['total'], t['next']
        ))

if __name__ == '__main__':
    main()
