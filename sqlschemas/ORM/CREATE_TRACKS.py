import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence


#-------[  Import From Other Modules   ]---------
from common_base import Base, engine
from common_orms import Host, User, UserItem, Resource, Reference



# ==============================================================
# >>>>>>>>>>>>>[    Independent Tables     ] >>>>>>>>>>>>>>>>>>>
# ==============================================================


class Track_SPT(Resource):
    __tablename__ = 'spotify_Tracks'

    abid = Column('album_id', String)
    atids = Column('artist_ids', String)

    disc_number = Column('disc_number', Integer)
    duration_ms = Column('duration_ms', Integer)
    markets = Column('available_markets', String)
    preview_url = Column('preview_url', String)
    popularity = Column('popularity', Integer)
    explicit = Column('explicit', Boolean)
    uri = Column('uri', String)
    href = Column('href', String)
    external_urls = Column('external_urls', String)
    is_local = Column('is_local', Boolean)


    @classmethod
    def add(cls, session, jsondata):
        j = jsondata['track']
        item = cls(
            id = j['id'],
            name = j['name'],
            abid = j['album']['id'],
            atids = ','.join([ a['id'] for a in j['artists'] ]),
            disc_number = j['disc_number'],
            duration_ms = j['duration_ms'],
            markets = ','.join([ m for m in j['available_markets'] ]),
            preview_url = j['preview_url'],
            popularity = j['popularity'],
            explicit = j['explicit'],
            uri = j['uri'],
            href = j['href'],
            external_urls = j['external_urls']['spotify'],
            is_local = j['is_local']
        )
        session.merge( item )   #Merge existing data
        #session.commit()  #-> Better to commit after multiple inserts

        return item


class Track_MBZ(Resource):
    __tablename__ = 'musicbrainz_Tracks'

class Track_FS(Resource):
    __tablename__ = 'filesystem_tracks'





# =====================================================================
# >>>>>>>>>>>>>>>>>>[    User Table     ] >>>>>>>>>>>>>>>>>>>>>>>>>>>>
# =====================================================================



class UserTrack(UserItem):
    """[  User's favorite tracks  ]
    :PKs: [ref_id, uid]
    :field last_played: Last time played the track
    :field added_at: Time added to the source library
    :field rate: Personal rating to the track
    :field memo: Personal comments
    :staticmethod add_from_spotify:
    """
    __tablename__ = 'u_Tracks'
    src_type = 'track'

    uid = Column('uid', String, ForeignKey('u_Users.uid'), primary_key=True)
    ref_id = Column('ref_id', String, ForeignKey('references.ref_id'), primary_key=True)

    last_played = Column('last_played', String)
    added_at = Column('added_at', String)
    count = Column('count', Integer)
    rate = Column('rate', Integer)
    memo = Column('memo', String)

    @classmethod
    def add(cls, session, uid, ref_id, jsondata):
        item = cls(
            uid = uid,
            ref_id = ref_id,
            last_played = None,
            added_at = jsondata['added_at'],
            count = 0,
            rate = 0,
            memo = ''
        )
        session.merge( item )
        #session.commit()  #-> Better to commit after multiple inserts
        return item






# ==============================================================
# >>>>>>>>>>>>>>>>>>>[    METHODS     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================



# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================



def main():
    #------- Start of Data Submitting ---------

    # Clearout all existing tables
    try:
        Track_SPT.__table__.drop(engine)
        Track_MBZ.__table__.drop(engine)
        Track_FS.__table__.drop(engine)
        UserTrack.__table__.drop(engine)
    except Exception as e:
        print('Error on dropping Track tables.')

    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)

    # Declare a common session for multiple files
    session = sessionmaker(bind=engine, autoflush=False)()

    # Get a user
    user = session.query(User).first()
    # Get a host
    h1 = session.query(Host).first()

    # Start of Data Insersions --------{
    import os, json
    cwd = os.path.split(os.path.realpath(__file__))[0]
    with open('{}/spotify/jsondumps-full/get_user_tracks.json'.format(os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )

    # Add user tracks
    UserTrack.add_items(
        session, h1.id, user.uid,
        data['items'], Track_SPT
    )
    # }------- End of Data Insersions


    session.commit()
    session.close()
    #------- End of Data Submitting ---------


if __name__ == '__main__':
    main()



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
