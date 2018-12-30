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




print('[ OK ] __IMPORTED__: {}'.format(__name__))
