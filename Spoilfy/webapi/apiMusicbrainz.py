#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:
#   - pip install xmltodict

import xmltodict
import requests


_ROOT = 'http://musicbrainz.org/ws/2'
_APP = {'User-Agent':'Spoilfy/0.0.1 (solomonxiewise@gmail)'}
_params = {'fmt':'json','limit':3}

def _get(url, params={}):
    """ [ Send HTTP Request & Get Response ]
    """
    params.update( _params )
    r = requests.get(url, headers=_APP, params=params)
    print( '[SEARCHING]', params, r.url )
    # return xmltodict.parse(r.content)
    return r.json()

def _qstr(query):
    """[ Get formated Query-String ]
        example: 'name:bigbang AND country:Norway'
    """
    return ' AND '.join(
        ['{0}:{1}'.format(k,v) for k,v in query.items()]
    )

def _confidence():
    pass



# [ SEARCHING ]
def _search_tracks(**query):
    url = '{}/recording'.format(_ROOT)
    params = {
        'query':_qstr(query),
        'inc':'artist-credits+isrcs+releases'
    }
    return _get(url, params)
def _search_album(**query):
    url = '{}/release'.format(_ROOT)
    params = {
        'query':_qstr(query),
        'inc': 'artist-credits+labels+discids+recordings'
    }
    return _get(url, params)
def _search_artist(**query):
    url = '{}/artist'.format(_ROOT)
    params = { 'query':_qstr(query), 'inc': 'aliases' }
    return _get(url, params)



# [ BEST MATCH: 1 RESULT ]
def best_match_track(**query):
    results = _search_tracks(**query)
    # Filter out the best match
    matches = sorted(results.get('recordings'),
        key=lambda o: o.get('score',0), reverse=True
    )
    best = matches[0] if matches else None
    return best
def best_match_album(**query):
    results = _search_album(**query)
    # Filter out the best match
    matches = sorted(results.get('releases'),
        key=lambda o: o.get('score',0), reverse=True
    )
    best = matches[0] if matches else None
    return best
def best_match_artist(**query):
    results = _search_artist(**query)
    # Filter out the best match
    matches = sorted(results.get('artists'),
        key=lambda o: o.get('score',0), reverse=True
    )
    best = matches[0] if matches else None
    return best


# [ GET INFO WITH SPECIFIC ID ]
def get_a_track(id):
    url = '{}/recording/{}'.format(_ROOT, id)
    params = { 'inc':'artist-credits+isrcs+releases' }
    return _get(url, params)
def get_an_album(id):
    url = '{}/release'.format(_ROOT)
    params = { 'inc': 'artist-credits+labels+discids+recordings' }
    return _get(url, params)
def get_an_artist(id):
    url = '{}/artist'.format(_ROOT)
    params = { 'inc': 'aliases' }
    return _get(url, params)



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
