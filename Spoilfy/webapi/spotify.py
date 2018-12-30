#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:
#   -

import json
import requests
from auth import Oauth2



class WebAPI:
    """ [ Common WebAPI Operations ]

    """
    pass


class SpotifyAPI(WebAPI):
    """ [  ]

    """
    ROOT = 'https://api.spotify.com/v1'

    def __init__(self, appdata):
        auth = Oauth2(appdata)
        self.token = auth.auto_fetch_token()
        self.headers = auth.add_token_to_headers({})

    def _get(self, url):
        r = requests.get(url, headers=self.headers)
        jsondata = r.json() if r else None
        return jsondata

    def _iterate(self, url, key=None):
        r = requests.get(url, headers=self.headers)
        jsondata = r.json() if r else None
        yield jsondata

        # Get paging info
        paging = jsondata[key] if key else jsondata
        next = paging['next']
        # Recursively retrive next page & yield result
        if next:
            yield from self._iterate(next, key)


    def get_my_profile(self):
        return self._get('{}/me'.format(self.ROOT))

    def get_my_tracks(self):
        return self._iterate('{}/me/tracks'.format(self.ROOT))

    def get_my_albums(self):
        return self._iterate('{}/me/albums'.format(self.ROOT))

    def get_my_artists(self):
        return self._iterate(
            '{}/me/following?type=artist'.format(self.ROOT),
            key='artists'
        )



print('[ OK ] __IMPORTED__: {}'.format(__name__))
