#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:
#   -

import json
import requests
from authlib.client import OAuth2Session



class WebAPI:
    """ [ Common WebAPI Operations ]

    """
    pass


class SpotifyAPI(WebAPI):
    """ [  ]

    """
    ROOT = 'https://api.spotify.com/v1'

    def __init__(self, appdata):
        auth = SpotifyOAuth2(appdata)
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


class SpotifyOAuth2:
    """ [ WebAPI Oauth 2.0 authentication ]

    """

    def __init__(self, appdata):
        # App's info
        self.client_id = appdata['client_id']
        self.client_secret = appdata['client_secret']
        self.scope = appdata['scope']
        self.redirect_uri = appdata['redirect_uri']
        self.authorize_url = appdata['authorize_url']
        self.access_token_url = appdata['access_token_url']
        self.cookies = appdata['cookies']

        # Dynamic properties
        self.session = None
        self.auth_uri = None
        self.state = None
        self.callback = None
        self.tokens = None
        self.token = None
        self.refersh_token = None

    def auto_fetch_token(self):
        # Auto-fetch access_token
        self.auth_uri, self.state = self.get_auth_uri()
        self.callback = self.get_callback()
        self.tokens = self.fetch_tokens()
        print('[ OK ] Authenticated.')
        # print( '[TOKEN]:{}'.format(self.tokens['access_token']) )

        return self.tokens['access_token']

    def get_auth_uri(self):
        """ [ Generate auth URL for user to login and authorize ]

        """
        # Create session
        self.session = OAuth2Session(
            self.client_id, self.client_secret,
            scope=self.scope, redirect_uri=self.redirect_uri
        )
        # Generate auth url for requests
        return self.session.create_authorization_url(
            self.authorize_url
        )

    def get_callback(self):
        """ [ Test only. Get CODE from callback URL ]

        """
        cookies = dict([line.split("=", 1) for line in self.cookies.strip().split("; ")])
        # Request API server / Or open browser manually
        try:
            r = requests.get(self.auth_uri, cookies=cookies, allow_redirects=True)
            for jump in r.history:
                print( jump.status_code, jump.url )
        except requests.exceptions.ConnectionError as e:
            #print( '[Final URL]: ', e.request.url )
            return e.request.url

    def fetch_tokens(self):
        # Fetch Tokens (in dict format)
        tokens = self.session.fetch_access_token(
            self.access_token_url,
            authorization_response = self.callback
        )
        print('[ OK ] Token retrived.')
        return tokens

    def refresh_tokens(self, refresh_token):
        # Create new session
        self.session = OAuth2Session(
            client_id, client_secret, token=tokens,
            scope=scope, redirect_uri=redirect_uri, state=self.state
        )
        # Refresh tokens
        tokens = self.session.refresh_token(
            self.access_token_url, refresh_token=self.tokens['refresh_token']
        )
        print('[ OK ] Token refreshed.')

        return tokens

    def add_token_to_headers(self, headers={}):
        headers['Authorization'] = 'Bearer {}'.format(
            self.tokens['access_token']
        )
        return headers

print('[ OK ] __IMPORTED__: {}'.format(__name__))
