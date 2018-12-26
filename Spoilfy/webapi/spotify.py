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


class SpotifyAPI(WebAPI):
    """

    """

    def __init__(self, appdata):
        auth = Oauth2(appdata)
        self.token = auth.auto_fetch_token()
        self.headers = auth.add_token_to_headers({})

    def _get(self, url):
        r = requests.get(url, headers=self.headers)
        jsondata = r.json() if r else None
        return jsondata
    
    def iterate(self, url):
        r = requests.get(url, headers=self.headers)
        jsondata = r.json() if r else None
        yield jsondata

        # Get paging info
        limit = jsondata['limit']
        offset = jsondata['offset']
        total = jsondata['total']
        next = jsondata['next']
        print('At {} / {}, {} per page, Next URL: \n\t{}'.format(
            offset, total, limit, next
        ))
        if next:
            yield from self.iterate(next)


    def get_my_profile(self):
        return self._get('https://api.spotify.com/v1/me')

    def get_my_tracks(self):
        return self.iterate('https://api.spotify.com/v1/me/tracks')




# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

def main():
    # Get auth info
    with open('./.spotify_app.json', 'r') as f:
        data = json.loads( f.read() )

    api = SpotifyAPI(data)
    #print( api.get_my_profile()['display_name'] )
    api.get_my_tracks()
    for t in api.get_my_tracks():
        continue

if __name__ == '__main__':
    main()


print('[ OK ] __IMPORTED__: {}'.format(__name__))
