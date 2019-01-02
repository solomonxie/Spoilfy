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
    print( '[FETCHING]', params, r.url )
    # return xmltodict.parse(r.content)
    return r.json()

def _qs(query):
    """[ Get formated query string ]
        example: 'name:bigbang AND country:Norway'
    """
    return ' AND '.join(
        ['{0}:{1}'.format(k,v) for k,v in query.items()]
    )

# [Tracks]
def search_tracks(**query):
    return _get(ROOT+'/recording',
        params={'query':_qs(query)}
    )

# [Albums]
def search_albums(**query):
    return _get(ROOT+'/release',
        params={'query':_qs(query)}
    )

# [Artists]
def search_artists(**query):
    return _get(ROOT+'/artist',
        params={'query':_qs(query)}
    )




print('[  OK  ] __IMPORTED__: {}'.format(__name__))
