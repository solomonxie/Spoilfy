
import os
import json
import musicbrainzngs as mb

with open('./.client_secret.json', 'r') as f:
    jsondata = json.loads( f.read() )
    user_name = jsondata['user_name']
    user_pass = jsondata['user_pass']
    app_name = jsondata['app_name']
    app_version = jsondata['app_version']
    app_url = jsondata['app_url']
    host_url = jsondata['host_url']

# Login
mb.auth(user_name, user_pass)

# Set up an app
mb.set_useragent(app_name, app_version, app_url)

# Sign a host engine to search from
mb.set_hostname(host_url)

# Search artist
artists = mb.search_artists(artist="big bang", type="group", country="Norway")

for a in artists['artist-list']:
    print( a['name'] )
