#!/usr/bin/env python3

# NOT WORKING YET !!!!!!!!!!!
# NOT WORKING YET !!!!!!!!!!!
# NOT WORKING YET !!!!!!!!!!!

import json
# and now no methods require the async/await syntax.
import spotify.sync as spotify

# Get auth info
with open('./.client_secret.json', 'r') as f:
    data = json.loads( f.read() )

client_id = data['client_id']
client_secret = data['client_secret']
scope = data['scope']
redirect_uri = data['redirect_uri']
authorize_url = data['authorize_url']
access_token_url = data['access_token_url']

client = spotify.Client(client_id, client_secret)

async def example():
    drake = await client.get_artist('3TVXtAsR1Inumwj472S9r4')

    for track in await drake.top_tracks():
        print(repr(track))

