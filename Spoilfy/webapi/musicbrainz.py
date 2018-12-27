#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:
#   - pip install xmltodict

import xmltodict
import requests


class MusicBrainzAPI:
    """ [  ]

    """
    ROOT = 'http://musicbrainz.org/ws/2'
    APP = {'User-Agent':'Spoilfy/0.0.1 (solomonxiewise@gmail)'}

    def _get(self, url, params={}):
        r = requests.get(url, headers=self.APP, params=params)
        print( '[FETCHING]', params, r.url )
        return xmltodict.parse(r.content)

    def _qs(self, query):
        """[ Get formated query string ]
            example: 'name:bigbang AND country:Norway'
        """
        return ' AND '.join(
            ['{0}:{1}'.format(k,v) for k,v in query.items()]
        )

    # [Tracks]
    def search_tracks(self, **query):
        return self._get(self.ROOT+'/recording',
            params={'query':self._qs(query)}
        )

    # [Albums]
    def search_albums(self, **query):
        return self._get(self.ROOT+'/release',
            params={'query':self._qs(query)}
        )

    # [Artists]
    def search_artists(self, **query):
        return self._get(self.ROOT+'/artist',
            params={'query':self._qs(query)}
        )



# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

def main():
    mba = MusicBrainzAPI()

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

print('[ OK ] __IMPORTED__: {}'.format(__name__))
