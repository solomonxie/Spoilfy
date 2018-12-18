import uuid

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence


#-------[  Import From Other Modules   ]---------
from common_base import Base, engine, session
from CREATE_HOSTS import Host
from CREATE_USERS import User



# ==============================================================
# >>>>>>>>>>>>>[    Independent Tables     ] >>>>>>>>>>>>>>>>>>>
# ==============================================================


class TrackSource(Base):
    """
    Abstract ORM class.
        Independent table, without any setup to relate User tables
        Manually search by id if needed.
    """
    __abstract__ = True

    id = Column('id', String, primary_key=True)
    name = Column('name', String)
    abid = Column('album_id', String)
    atids = Column('artist_ids', String)
    disc_number = Column('disc_number', Integer)
    duration_ms = Column('duration_ms', Integer)

    @classmethod
    def add_tracks(cls, session, jsondata):
        pass

class Track_SPT(TrackSource):
    __tablename__ = 'spotify_Tracks'

    markets = Column('available_markets', String)
    preview_url = Column('preview_url', String)
    popularity = Column('popularity', Integer)
    explicit = Column('explicit', Boolean)
    uri = Column('uri', String)
    href = Column('href', String)
    external_urls = Column('external_urls', String)
    is_local = Column('is_local', Boolean)

    @classmethod
    def add_tracks(cls, session, jsondata):
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


class Track_MBZ(TrackSource):
    __tablename__ = 'musicbrainz_Tracks'

class Track_FS(TrackSource):
    __tablename__ = 'filesystem_tracks'


class TrackRef(Base):
    """
    :field id: Primary key only.
    :field ref_id: Unique Reference ID, as a connector to multiple sources.
    :field host_id: Identify the Source Provider
    :field src_id: Source ID, to be used with host_id: track 'Hey Jude' on Spotify.
    """
    __tablename__ = 'ref_Tracks'

    ref_id = Column('ref_id', String, nullable=False)  #>> unique reference ID
    host_id = Column('host_id', Integer, ForeignKey('hosts.id'), primary_key=True)
    src_id = Column('src_id', String, primary_key=True, nullable=False)  #>> dynamic | not speicify FK

    #def __init__(self, ref_id, host_id, src_id):
    #    if not ref_id:
    #        self.id = str(uuid.uuid1())


    @staticmethod
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
        print( '[  OK  ] Inserted {} references.'.format(len(references)) )

        return references


# ==============================================================
# >>>>>>>>>>>>>>>>>>>[    METHODS     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================






# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================



def main():
    #------- Start of Data Submitting ---------

    # Clearout all existing tables
    Base.metadata.drop_all(engine)

    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)

    h1 = session.query(Host).first()

    # Start of Data Insersions --------{
    import os, json
    cwd = os.path.split(os.path.realpath(__file__))[0]
    with open('{}/spotify/jsondumps-full/get_user_tracks.json'.format(os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )

    tracks = Track_SPT.add_tracks(session, data)
    refs = TrackRef.add_track_reference(session, tracks, 1)

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
