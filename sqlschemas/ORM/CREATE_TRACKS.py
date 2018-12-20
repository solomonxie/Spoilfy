import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence


#-------[  Import From Other Modules   ]---------
from common_base import Base, engine
from common_orms import Resource, Reference
from CREATE_USERS import User
from CREATE_HOSTS import Host



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
    except Exception as e:
        print('Error on dropping Track tables.')

    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)

    # Declare a common session for multiple files
    session = sessionmaker(bind=engine, autoflush=False)()

    h1 = session.query(Host).first()

    # Start of Data Insersions --------{
    import os, json
    cwd = os.path.split(os.path.realpath(__file__))[0]
    with open('{}/spotify/jsondumps-full/get_user_tracks.json'.format(os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )

    tracks = Track_SPT.add_sources(session, data['items'])
    refs = Reference.add_references(session, 'track', h1.id, tracks)
    # }------- End of Data Insersions


    session.commit()
    session.close()
    #------- End of Data Submitting ---------


if __name__ == '__main__':
    main()



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
