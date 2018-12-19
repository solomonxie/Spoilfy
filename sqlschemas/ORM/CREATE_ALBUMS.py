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
    tids = Column('track_ids', String)
    album_type = Column('album_type', String)
    release_date = Column('release_date', String)
    release_date_precision = Column('release_date_precision', String)

    total_tracks = Column('total_tracks', Integer)
    lable = Column('lable', String)
    popularity = Column('popularity', Integer)
    copyrights = Column('copyrights', String)
    uri = Column('uri', String)
    href = Column('href', String)
    external_urls = Column('external_urls', String)
    external_ids = Column('external_ids', String)

    #tracks = Column('tracks', String)  #>>For [Track_SPT]
    #artists = Column('artists', String)  #>>For [Artist_SPT]

    @classmethod
    def add_sources(cls, session, jsondata):
        """[ Add Spotify's Albums ]
        :param session: SQLAlchemy session object connected to DB
        :param String jsondump: JSON data in string format
        :return: Class instances of track resources
        """
        all_sources = []
        for data in jsondata['items']:
            item = cls.add(session, data)
            all_sources.append(item)

        session.commit()
        print( '[  OK  ] Inserted {} Albums.'.format(len(all_sources)) )

        return all_sources

    @classmethod
    def add(cls, session, jsondata):
        d = jsondata['album']
        item = cls(
            id = d['id'],
            name = d['name'],
            atids = ','.join([ a['id'] for a in d['artists'] ]),
            tids = ','.join([ a['id'] for a in d['tracks']['items'] ]),
            album_type = d['album_type'],
            release_date = d['release_date'],
            release_date_precision = d['release_date_precision'],
            total_tracks = d['total_tracks'],
            lable = d['label'],
            popularity = d['popularity'],
            copyrights = str(d['copyrights']),
            uri = d['uri'],
            href = d['href'],
            external_urls = str(d['external_urls']),
            external_ids = str(d['external_ids'])
        )
        session.merge( item )
        #session.commit()
        return item


class Album_MBZ(Source):
    __tablename__ = 'musicbrainz_Albums'


class Album_FS(Source):
    __tablename__ = 'filesystem_Albums'



class AlbumRef(Reference):
    __tablename__ = 'ref_Albums'

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
    try:
        AlbumRef.__table__.drop(engine)
        Album_SPT.__table__.drop(engine)
        Album_MBZ.__table__.drop(engine)
        Album_FS.__table__.drop(engine)
    except Exception as e:
        print('Error on dropping Album tables.')

    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)

    # Declare a common session for multiple files
    session = sessionmaker(bind=engine, autoflush=False)()

    h1 = session.query(Host).first()

    # Start of Data Insersions --------{
    import os, json
    cwd = os.path.split(os.path.realpath(__file__))[0]
    with open('{}/spotify/jsondumps-full/get_user_albums.json'.format(os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )

    sources = Album_SPT.add_sources(session, data)
    refs = AlbumRef.add_references(session, h1.id, sources)

    session.commit()
    session.close()
    #------- End of Data Submitting ---------


if __name__ == '__main__':
    pass
    main()



print('[  OK  ] IMPORTED: {}'.format(__name__))
