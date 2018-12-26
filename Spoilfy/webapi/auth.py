#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import requests
from authlib.client import OAuth2Session


class Auth:
    """ [ Wrapped WebAPI Authentication Methods ]

    """
    pass


class Oauth2(Auth):
    """ [ WebAPI Oauth 2.0 authentication ]

    """

    def __init__(self, app):
        # App's info
        self.client_id = app['client_id']
        self.client_secret = app['client_secret']
        self.scope = app['scope']
        self.redirect_uri = app['redirect_uri']
        self.authorize_url = app['authorize_url']
        self.access_token_url = app['access_token_url']
        self.cookies = app['cookies']

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
        print( '[TOKEN]:{}'.format(self.tokens['access_token']) )

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
            print( '[Final URL]: ', e.request.url )
            return e.request.url

    def fetch_tokens(self):
        # Fetch Tokens (in dict format)
        return self.session.fetch_access_token(
            self.access_token_url,
            authorization_response = self.callback
        )

    def refresh_tokens(self, refresh_token):
        # Create new session
        self.session = OAuth2Session(
            client_id, client_secret, token=tokens,
            scope=scope, redirect_uri=redirect_uri, state=self.state
        )
        # Refresh tokens
        return self.session.refresh_token(
            self.access_token_url, refresh_token=self.tokens['refresh_token']
        )

    def add_token_to_headers(self, headers={}):
        headers['Authorization'] = 'Bearer {}'.format(
            self.tokens['access_token']
        )
        return headers

# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


def main():
    # Get auth info
    with open('./.spotify_app.json', 'r') as f:
        data = json.loads( f.read() )
    # Authenticate
    auth = Oauth2(data)
    token = auth.auto_fetch_token()
    print( auth.add_token_to_headers() )

if __name__ == '__main__':
    main()
