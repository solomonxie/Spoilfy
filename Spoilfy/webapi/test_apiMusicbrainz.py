#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest

from apiMusicbrainz import MusicbrainzAPI as mbz


# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


class TestMusicbrainzAPI(unittest.TestCase):

    def test_get_a_track(self):
        # track = mbz.get_a_track('4ae5ea82-31ef-4099-a315-3c2487d9dd32')
        # print( '\t[TRACK]:', track.get('title'), track.get('length') )
        pass

    def test_get_an_album(self):
        # album = mbz.get_an_album('d8507216-2261-4b18-a033-0a8628ecff9e')
        # print( '\t[ALBUM]:', album.get('title'), album.get('date') )
        pass

    def test_get_an_artist(self):
        # artist = mbz.get_an_artist('5b11f4ce-a62d-471e-81fc-a69a8278c7da')
        # print( '\t[ARTIST]:', artist.get('name'), artist.get('country') )
        pass

    def search_a_track(self):
        # track = mbz.best_match_track(name='Pristine')
        # print( '\t[TRACK]:', track.get('title'), track.get('score') )
        pass

    def search_an_album(self):
        # album = mbz.best_match_album(name='edendale', country='NO')
        # print( '\t[ALBUM]:', album.get('title'), album.get('score') )
        pass

    def search_an_artist(self):
        # artist = mbz.best_match_artist(name='bigbang', country='NO')
        # print( '\t[ARTIST]:', artist.get('name'), artist.get('country') )
        pass


class TestMusicbrainzXmlAPI:

    def test_xmlapi(self):
        # Search Tracks
        results = mbz.search_tracks(name='bigbang', country='NO')
        for obj in results['metadata']['recording-list']['recording']:
            print('\t[TRACK]:', obj['title'], obj['length'], obj['@id'])
        #obj = results['metadata']['artist-list']['artist'][0]

        # Search Albums
        results = mbz.search_albums(name='edendale', country='NO')
        #obj = results['metadata']['artist-list']['artist'][0]
        for obj in results['metadata']['release-list']['release']:
            print('\t[ALBUM]:', obj['title'], obj['date'], obj['@id'])

        # Search Artists
        results = mbz.search_artists(name='bigbang', country='NO')
        #obj = results['metadata']['artist-list']['artist'][0]
        for obj in results['metadata']['artist-list']['artist']:
            print('\t[ARTIST]:', obj['country'], obj['name'], obj['@id'])


if __name__ == '__main__':
    unittest.main()
