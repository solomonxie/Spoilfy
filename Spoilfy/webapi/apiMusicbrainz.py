#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:
#   - pip install xmltodict

import xmltodict
import requests


ROOT = 'http://musicbrainz.org/ws/2'
APP = {'User-Agent':'Spoilfy/0.0.1 (solomonxiewise@gmail)'}
oparams = {'fmt':'json','limit':3,'inc':''}

def _get(url, params={}):
    params.update(oparams)
    r = requests.get(url, headers=APP, params=params)
    print( '[SEARCHING]', params, r.url )
    # return xmltodict.parse(r.content)
    return r.json()

def _qstr(query):
    """[ Get formated query string ]
        example: 'name:bigbang AND country:Norway'
    """
    return ' AND '.join(
        ['{0}:{1}'.format(k,v) for k,v in query.items()]
    )

def _confidence():
    pass

# [Tracks]
def _search_tracks(**query):
    return _get(
        url = '{}/recording'.format(ROOT),
        params = {'query':_qstr(query)}
    )
def best_match_track(**query):
    results = _search_tracks(**query)
    # Filter out the best match
    matches = sorted(results.get('recordings'),
        key=lambda o: o.get('score',0), reverse=True
    )
    best = matches[0] if matches else None
    return best

# [Albums]
def _search_album(**query):
    return _get(
        url = '{}/release'.format(ROOT),
        params={'query':_qstr(query)}
    )
def best_match_album(**query):
    results = _search_album(**query)
    # Filter out the best match
    matches = sorted(results.get('releases'),
        key=lambda o: o.get('score',0), reverse=True
    )
    best = matches[0] if matches else None
    return best

# [Artists]
def _search_artist(**query):
    return _get(
        url = '{}/artist'.format(ROOT),
        params={'query':_qstr(query)}
    )
def best_match_artist(**query):
    results = _search_artist(**query)
    # Filter out the best match
    matches = sorted(results.get('artists'),
        key=lambda o: o.get('score',0), reverse=True
    )
    best = matches[0] if matches else None
    return best




print('[  OK  ] __IMPORTED__: {}'.format(__name__))
