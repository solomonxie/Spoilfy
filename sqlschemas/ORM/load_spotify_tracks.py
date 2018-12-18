import os
import json

from CREATE_TRACKS5_string_id import *

cwd = os.path.split(os.path.realpath(__file__))[0]
engine = create_engine('sqlite:///{}/db_u_spoilfy.sqlite'.format(cwd))
session = sessionmaker(bind=engine, autoflush=False)()

# 1. Add Hosts
h1 = Host(name='Spotify',
        tbname_track='spotify_Tracks',
        tbname_album='spotify_Albums',
        tbname_artist='spotify_Artists',
        tbname_playlist='spotify_Playlists'
)
h2 = Host(name='MusicBrainz',
        tbname_track='musicbrainz_Tracks',
        tbname_album='musicbrainz_Albums',
        tbname_artist='musicbrainz_Artists',
        tbname_playlist='musicbrainz_Playlists'
)
session.add_all([h1, h2])
session.flush()  # Generate data for Dynamic fileds(primary key) to get values


# 2. Add Users
u1 = User(name='Jason')
u2 = User(name='David')
u3 = User(name='Sol')
session.add_all([u1,u2,u3])
session.flush()  # Generate data for Dynamic fileds(primary key) to get values



#===============================================================================
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>[  BEGIN  ]>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#===============================================================================


def get_tablename_for_track(session, host_id):
    """[ Return track's DB table name binded with Host ]
    :param session: SQLAlchemy session object connected to DB
    :param String jsondump: JSON data in string format
    :return : No return.
    """
    host = session.query(Host).filter(
        Host.id == host_id
    ).first()
    return host.tbname_track if host else None
#print( get_tablename_for_track(session, 1) )




def get_class_by_tablename(tablename):
    """[ Search class reference mapped to table. ]
    :param table_fullname: String with fullname of table.
    :return: Class reference or None.
    """
    for cls in Base._decl_class_registry.values():
        return cls if hasattr(cls, '__table__') and \
                cls.__table__.fullname == tablename else None
#print( get_class_by_tablename('spotify_Tracks') )




def add_spotify_tracks(session, jsondata):
    """[ Add Spotify's Tracks ]
    :param session: SQLAlchemy session object connected to DB
    :param String jsondump: JSON data in string format
    :return: Class instances of track resources
    """
    all_tracks = []
    for i,data in enumerate(jsondata['items']):
        t = data['track']
        track= Track_SPT(
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
        session.merge(track)   #Merge existing data
        all_tracks.append(track)

    session.commit()
    print( '[  OK  ] Inserted {} tracks.'.format(len(all_tracks)) )

    return all_tracks

#with open('{}/spotify/jsondumps/get_user_tracks.json'.format(os.path.dirname(cwd)), 'r') as f:
#    data = json.loads( f.read() )
##add_spotify_tracks(session, data)
#
#tracks = add_spotify_tracks(session, data)




def add_track_reference(session, tracks, host_id):
    references = []
    for t in tracks:
        ref = TrackRef(
            ref_id=str(uuid.uuid1()),
            src_id=t.id,
            host_id=host_id
        )
        session.merge(ref)
        references.append(ref)

    session.commit()
    print( '[  OK  ] Inserted references.' )

    return references

#refs = add_track_reference(session, tracks, 1)

#>> Multiple Primary Key Conflict test
#ref_conflict = TrackRef(
#    src_id=refs[0].src_id,
#    host_id=refs[0].host_id,
#    ref_id=refs[0].ref_id
#)
#session.merge(ref_conflict)
#session.commit()




def user_add_spotify_tracks(session, uid, jsondata):
    tracks = add_spotify_tracks(session, jsondata)
    refs = add_track_reference(session, tracks, 1)
    # Add User Tracks
    user = session.query(User).filter(User.uid==uid).first()
    print('[  OK  ] User: ',user.name)
    user_tracks = []
    for ref in refs:
        ut = UserTrack(
            uid = user.uid,
            ref_id = ref.ref_id,
            last_played = None,
            added_at = None,
            count = 0,
            rate = 0,
            memo = ''
        )
        session.merge(ut)
        user_tracks.append(ut)

    session.commit()
    print( '[  OK  ] Inserted User Tracks.' )

    return user_tracks
    

with open('{}/spotify/jsondumps-full/get_user_tracks.json'.format(os.path.dirname(cwd)), 'r') as f:
    data = json.loads( f.read() )
    user_add_spotify_tracks(session, 1, data)



print('[  OK  ] {}'.format(__name__))
