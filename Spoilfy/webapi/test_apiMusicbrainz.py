#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest

import musicbrainz as mba



# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


def test_jsonapi():
    # Search Tracks
    results = mba.search_tracks(name='Pristine', country='NO')
    for obj in results.get('recordings'):
        print( '\t[TRACK]:',
            obj.get('title'), obj.get('length'),
            obj.get('id'), obj.get('score')
        )

    # Search Albums
    results = mba.search_albums(name='edendale', country='NO')
    for obj in results.get('releases'):
        print( '\t[ALBUM]:',
            obj.get('title'), obj.get('date'),
            obj.get('id'), obj.get('score')
        )

    # Search Artists
    results = mba.search_artists(name='bigbang', country='NO')
    for obj in results.get('artists'):
        print( '\t[ARTIST]:',
            obj.get('country'), obj.get('name'),
            obj.get('id'), obj.get('score')
        )

def test_xmlapi():

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
    # test_xmlapi()
    test_jsonapi()
