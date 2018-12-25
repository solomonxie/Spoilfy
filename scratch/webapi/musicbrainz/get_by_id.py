import json
import musicbrainzngs as mb


#====================================================================
#>>>>>>>>>>>>>>>>>>>>>>>>>>>[ LOG IN ]>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#====================================================================

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


#====================================================================
#>>>>>>>>>>>>>>>>>>>>>>>[ SEARCH API ]>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#====================================================================

# -----------[ Get By ID ]------------------

# Get an artist
id = 'e86ab653-bec8-46f3-b4b6-a1a866919ef6'
artist = mb.get_artist_by_id(id)['artist']
print( '[ Artist Name ]:', artist['name'] )



# Get an album (Release)
id = 'ccd708f2-06f5-43d4-8396-032dc7eb1883'
album = mb.get_release_by_id(id)['release']
print( '[ Album Title ]:', album['title'] )


# Get a track (Recording)
id = 'c216f892-e329-4986-9373-6d95660801d6'
track = mb.get_recording_by_id(id)['recording']
print( '[ Track Title ]:', track['title'] )
