#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest

import apiMusicbrainz as mbz



# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


def test_jsonapi():
    # Search Tracks
    track = mbz.best_match_track(name='Pristine')
    print( '\t[TRACK]:',
        track.get('title'), track.get('length'),
        track.get('id'), track.get('score')
    )

    # Search Albums
    album = mbz.best_match_album(name='edendale', country='NO')
    print( '\t[ALBUM]:',
        album.get('title'), album.get('date'),
        album.get('id'), album.get('score')
    )

    # Search Artists
    artist = mbz.best_match_artist(name='bigbang', country='NO')
    print( '\t[ARTIST]:',
        artist.get('country'), artist.get('name'),
        artist.get('id'), artist.get('score')
    )


def test_xmlapi():

    # Search Tracks
    results = mbz.search_tracks(name='bigbang', country='NO')
    for obj in results['metadata']['recording-list']['recording']:
        print( '\t[TRACK]:', obj['title'], obj['length'], obj['@id'] )
    #obj = results['metadata']['artist-list']['artist'][0]

    # Search Albums
    results = mbz.search_albums(name='edendale', country='NO')
    #obj = results['metadata']['artist-list']['artist'][0]
    for obj in results['metadata']['release-list']['release']:
        print( '\t[ALBUM]:', obj['title'], obj['date'], obj['@id'] )

    # Search Artists
    results = mbz.search_artists(name='bigbang', country='NO')
    #obj = results['metadata']['artist-list']['artist'][0]
    for obj in results['metadata']['artist-list']['artist']:
        print( '\t[ARTIST]:', obj['country'], obj['name'], obj['@id'] )



if __name__ == '__main__':
    # test_xmlapi()
    test_jsonapi()
