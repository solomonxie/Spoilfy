import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence


#-------[  Import From Other Modules   ]---------
from common_base import Base, engine
from common_orms import Source, Reference
from CREATE_HOSTS import Host
from CREATE_USERS import User



# ==============================================================
# >>>>>>>>>>>>>[    Independent Tables     ] >>>>>>>>>>>>>>>>>>>
# ==============================================================


class Track_SPT(Source):
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
    def add_sources(cls, session, jsondata):
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


class Track_MBZ(Source):
    __tablename__ = 'musicbrainz_Tracks'

class Track_FS(Source):
    __tablename__ = 'filesystem_tracks'


class TrackRef(Reference):
    __tablename__ = 'ref_Tracks'

    host_id = Column('host_id', Integer, ForeignKey('hosts.id'), primary_key=True)



# ==============================================================
# >>>>>>>>>>>>>>>>>>>[    METHODS     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================






# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================



def main():
    #------- Start of Data Submitting ---------

    # Clearout all existing tables
    TrackRef.__table__.drop(engine)
    Track_SPT.__table__.drop(engine)
    Track_MBZ.__table__.drop(engine)
    Track_FS.__table__.drop(engine)

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

    tracks = Track_SPT.add_sources(session, data)
    refs = TrackRef.add_references(session, h1.id, tracks)

    #>> Multiple Primary Key Conflict test
    #ref7 = TrackRef(ref_id=t3.ref_id, src_id=src1_3.id, host_id=h2.id)
    #session.add(ref7)
    #session.flush()  # Generate data for Dynamic fileds(primary key) to get values
    # }------- End of Data Insersions


    session.commit()
    session.close()
    #------- End of Data Submitting ---------


if __name__ == '__main__':
    main()



print('[  OK  ] IMPORTED: {}'.format(__name__))
