#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import requests
from auth import Oauth2



class WebAPI:
    """ [ Common WebAPI Operations ]

    """
    pass


def retrive(func):
    """ [ Decorator ]

    """
    def wrapper(*args, **kargs):
        #...
        result = func(*args, **kargs)
        #...
        return result
    return wrapper



class SpotifyAPI(WebAPI):
    """

    """

    def __init__(self, appdata):
        auth = Oauth2(appdata)
        self.token = auth.auto_fetch_token()
        self.headers = auth.add_token_to_headers({})

    def get(self, url):
        r = requests.get(url, headers=self.headers)
        jsondata = r.json() if r else None
        return jsondata

    #@retrive
    def get_my_profile(self):
        return 'https://api.spotify.com/v1/me'




# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

def main():
    # Get auth info
    with open('./.spotify_app.json', 'r') as f:
        data = json.loads( f.read() )

    api = SpotifyAPI(data)
    print( api.get(api.get_my_profile()) )

if __name__ == '__main__':
    main()


print('[  OK  ] __IMPORTED__: {}'.format(__name__))
