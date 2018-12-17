import os
import json
cwd = os.path.split(os.path.realpath(__file__))[0]


from CREATE_TRACKS5_string_id import *

engine = create_engine('sqlite:///{}/db_u_spoilfy.sqlite'.format(cwd), echo=False)
session = sessionmaker(bind=engine, autoflush=False)()




path = '{}/spotify/jsondumps/get_user_tracks.json'.format(os.path.dirname(cwd))

with open(path, 'r') as f:
    data = json.loads(f.read())

# Add Spotify's Tracks
for i,track in enumerate(data['items']):
    t = track['track']
    source = Track_SPT(
        id = t['id'],
        name = t['name'],
        abid = t['album']['id'],
        atids = ','.join([ a['id'] for a in t['artists'] ]),
        disc_number = t['disc_number'],
        duration_ms = t['duration_ms'],
        markets = ','.join([ m for m in t['available_markets'] ]),
        preview_url = t['preview_url'],
        popularity = t['popularity'],
        explicit = t['explicit'],
        uri = t['uri'],
        href = t['href'],
        external_urls = t['external_urls']['spotify'],
        is_local = t['is_local']
    )
    session.add(source)

session.commit()


