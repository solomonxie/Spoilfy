#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:
#   - pip install xmltodict

import xmltodict
import requests

_ROOT = 'http://musicbrainz.org/ws/2'
_APP = {'User-Agent': 'Spoilfy/0.0.1 (solomonxiewise@gmail)'}
_params = {'fmt': 'json'}


class MusicbrainzAPI:

    @classmethod
    def _get(cls, url, params={}):
        """ [ Send HTTP Request & Get Response ]
        """
        params.update(_params)
        r = requests.get(url, headers=_APP, params=params)
        print('[SEARCHING]', params, r.url)
        # return xmltodict.parse(r.content)
        return r.json()

    @classmethod
    def _qstr(cls, query):
        """[ Get formated Query-String ]
            example: 'name:bigbang AND country:Norway'
        """
        return ' AND '.join(
            ['{0}:{1}'.format(k, v) for k, v in query.items()]
        )

    @classmethod
    def _confidence(cls):
        pass

    # [ SEARCHING ]
    @classmethod
    def _search_tracks(cls, **query):
        url = '{}/recording'.format(_ROOT)
        params = {
            'query': cls._qstr(query), 'limit': 3,
            'inc': 'artist-credits+isrcs+releases'
        }
        return cls._get(url, params)

    @classmethod
    def _search_album(cls, **query):
        url = '{}/release'.format(_ROOT)
        params = {
            'query': cls._qstr(query), 'limit': 3,
            'inc': 'artist-credits+labels+discids+recordings'
        }
        return cls._get(url, params)

    @classmethod
    def _search_artist(cls, **query):
        url = '{}/artist'.format(_ROOT)
        params = {'query': cls._qstr(query), 'limit': 3, 'inc': 'aliases'}
        return cls._get(url, params)

    # [ BEST MATCH: 1 RESULT ]
    @classmethod
    def best_match_track(cls, **query):
        results = cls._search_tracks(**query)
        # Filter out the best match
        matches = sorted(results.get('recordings', []),
                         key=lambda o: o.get('score', 0), reverse=True
                         )
        best = matches[0] if matches else None
        return best

    @classmethod
    def best_match_album(cls, **query):
        results = cls._search_album(**query)
        # Filter out the best match
        matches = sorted(results.get('releases', []),
                         key=lambda o: o.get('score', 0), reverse=True
                         )
        best = matches[0] if matches else None
        return best

    @classmethod
    def best_match_artist(cls, **query):
        results = cls._search_artist(**query)
        # Filter out the best match
        matches = sorted(results.get('artists', []),
                         key=lambda o: o.get('score', 0), reverse=True
                         )
        best = matches[0] if matches else None
        return best

    # [ GET SPECIFIC INFO WITH ID ]
    @classmethod
    def get_a_track(cls, id):
        url = '{}/recording/{}'.format(_ROOT, id)
        params = {'inc': 'artist-credits+isrcs+releases'}
        return cls._get(url, params)

    @classmethod
    def get_an_album(cls, id):
        url = '{}/release/{}'.format(_ROOT, id)
        params = {'inc': 'artist-credits+labels+discids+recordings'}
        return cls._get(url, params)

    @classmethod
    def get_an_artist(cls, id):
        url = '{}/artist/{}'.format(_ROOT, id)
        params = {'inc': 'aliases'}
        return cls._get(url, params)


print('[  OK  ] __IMPORTED__: {}'.format(__name__))
