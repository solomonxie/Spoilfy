import uuid
from datetime import datetime

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



class Album_SPT(Source):
    __tablename__ = 'spotify_Albums'

    atids = Column('artist_ids', String)
    album_type = Column('album_type', String)
    album_group = Column('album_group', String)
    release_date = Column('release_date', String)
    total_tracks = Column('total_tracks', Integer)
    release_date_precision = Column('release_date_precision', String)
    markets = Column('available_markets', String)
    href = Column('href', String)
    external_urls = Column('external_urls', String)
    uri = Column('uri', String)

    @classmethod
    def add_sources(cls, session, jsondata):
        """[ Add Spotify's Albums ]
        :param session: SQLAlchemy session object connected to DB
        :param String jsondump: JSON data in string format
        :return: Class instances of track resources
        """
        all_albums = []
        for i,d in enumerate(jsondata['items']):
            src = cls(
                id = d['id'],
                name = d['name'],
                album_type = d['album_type'],
                album_group = d['album_group'],
                atids = ','.join([ a['id'] for a in d['artists'] ]),
                release_date = d['release_date'],
                #release_date = datetime.strptime(d['release_date'], '%Y-%m-%d'),
                release_date_precision = d['release_date_precision'],
                total_tracks = d['total_tracks'],
                markets = ','.join([ m for m in d['available_markets'] ]),
                uri = d['uri'],
                href = d['href'],
                external_urls = d['external_urls']['spotify']
            )
            session.merge(src)
            all_albums.append(src)

        session.commit()
        print( '[  OK  ] Inserted {} Albums.'.format(len(all_albums)) )

        return all_albums


class Album_MBZ(Source):
    __tablename__ = 'musicbrainz_Album'


class Album_FS(Source):
    __tablename__ = 'filesystem_Album'



class AlbumRef(Reference):
    __tablename__ = 'ref_Album'

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
    AlbumRef.__table__.drop(engine)
    Album_SPT.__table__.drop(engine)
    Album_MBZ.__table__.drop(engine)
    Album_FS.__table__.drop(engine)

    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)

    # Declare a common session for multiple files
    session = sessionmaker(bind=engine, autoflush=False)()

    h1 = session.query(Host).first()

    # Start of Data Insersions --------{
    import os, json
    cwd = os.path.split(os.path.realpath(__file__))[0]
    with open('{}/spotify/jsondumps-full/get_artist_albums.json'.format(os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )

    sources = Album_SPT.add_sources(session, data)
    refs = AlbumRef.add_reference(session, sources, 1)

    #>> Multiple Primary Key Conflict test
    #ref7 = TrackRef(ref_id=t3.ref_id, src_id=src1_3.id, host_id=h2.id)
    #session.add(ref7)
    #session.flush()  # Generate data for Dynamic fileds(primary key) to get values
    # }------- End of Data Insersions


    session.commit()
    session.close()
    #------- End of Data Submitting ---------


if __name__ == '__main__':
    pass
    main()



print('[  OK  ] IMPORTED: {}'.format(__name__))
