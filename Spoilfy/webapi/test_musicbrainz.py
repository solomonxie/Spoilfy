#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest

from musicbrainz import MusicbrainzAPI



# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================



def main():
    mba = MusicbrainzAPI()

    # Search Tracks
    results = mba.search_tracks(name='bigbang', country='NO')
    for obj in results['metadata']['recording-list']['recording']:
        print( '\t[TRACK]:', obj['title'], obj['length'], obj['@id'] )
    #obj = results['metadata']['artist-list']['artist'][0]

    # Search Albums
    results = mba.search_albums(name='edendale', country='NO')
    #obj = results['metadata']['artist-list']['artist'][0]
    for obj in results['metadata']['release-list']['release']:
        print( '\t[ALBUM]:', obj['title'], obj['date'], obj['@id'] )

    # Search Artists
    results = mba.search_artists(name='bigbang', country='NO')
    #obj = results['metadata']['artist-list']['artist'][0]
    for obj in results['metadata']['artist-list']['artist']:
        print( '\t[ARTIST]:', obj['country'], obj['name'], obj['@id'] )



if __name__ == '__main__':
    main()
