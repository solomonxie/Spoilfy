#!/usr/bin/env python3

# NOT WORKING YET !!!!!!!!!!!
# NOT WORKING YET !!!!!!!!!!!
# NOT WORKING YET !!!!!!!!!!!

import spotipy

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify()

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])
