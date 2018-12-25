import os
import sys
import json

import requests
from authlib.client import OAuth2Session

# Get API's essential info
with open('./.client_secret.json', 'r') as f:
    data = json.loads( f.read() )

client_id = data['client_id']
client_secret = data['client_secret']
scope = data['scope']
redirect_uri = data['redirect_uri']
authorize_url = data['authorize_url']
access_token_url = data['access_token_url']


# Create Session
session = OAuth2Session(
    client_id, client_secret,
    scope=scope, redirect_uri=redirect_uri
)


# Generate auth url for requests
uri, state = session.create_authorization_url( authorize_url )



#headers = dict([line.split(': ',1) for line in s_headers.strip().split('\n')])
cookies = dict([line.split("=", 1) for line in data['cookies'].strip().split("; ")])




# Request API server / Or open browser manually
authorization_response = ''
try:
    print( '[Requesting Authentication]: {}'.format(uri) )
    r = requests.get(uri, cookies=cookies, allow_redirects=True)
    for jump in r.history:
        print( 'Status:[{}] on:{}'.format(jump.status_code, jump.url) )
except requests.exceptions.ConnectionError as e:
    print( '[Final URL]: ', e.request.url )
    authorization_response = e.request.url



# Fetch Tokens (in dict format)
if authorization_response:
    tokens = session.fetch_access_token(
        access_token_url,
        authorization_response=authorization_response
    )
    print( '[Tokens]:', tokens )

    # Make a header with Auth token
    H = {'Authorization': 'Bearer {}'.format(tokens['access_token'])}

    # API entry point
    api = 'https://api.spotify.com/v1/me/tracks?offset=0&limit=50'

    # Retrive an API  with TOKEN
    #r = requests.get(api, headers=H)
    #jsondata = r.json()
    #print(jsondata['limit'], '/', jsondata['total'])

    # Interate API
    next = api
    while next:
        # Retrive api
        r = requests.get(next, headers=H)
        jsondata = r.json()
        print( jsondata )
        # Get paging info
        limit = jsondata['limit']
        offset = jsondata['offset']
        total = jsondata['total']
        next = jsondata['next']
        print( 'At {} / {}, {} per page, Next URL: \n\t{}'.format(
            offset, total, limit, next)
        )
        sys.sleep(1)

