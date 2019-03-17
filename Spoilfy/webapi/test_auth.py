#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import json
import unittest

from auth import Oauth2

# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


def main():
    # Get auth info
    with open('./.spotify_app.json', 'r') as f:
        data = json.loads(f.read())
    # Authenticate
    auth = Oauth2(data)
    token = auth.auto_fetch_token()
    print(auth.add_token_to_headers())


if __name__ == '__main__':
    main()
