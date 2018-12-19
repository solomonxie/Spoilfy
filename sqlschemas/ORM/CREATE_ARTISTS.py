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



class Artist_SPT(Source):
    __tablename__ = 'spotify_Artists'

    atids = Column('artist_ids', String)
    markets = Column('available_markets', String)
    href = Column('href', String)
    external_urls = Column('external_urls', String)
    uri = Column('uri', String)

    @classmethod
    def add_sources(cls, session, jsondata):
        """[ Add Spotify's Artists ]
        :param session: SQLAlchemy session object connected to DB
        :param String jsondump: JSON data in string format
        :return: Class instances of track resources
        """
        all_artists = []
        for i,d in enumerate(jsondata['items']):
            src = cls(
                id = d['id'],
                name = d['name'],
                markets = ','.join([ m for m in d['available_markets'] ]),
                uri = d['uri'],
                href = d['href'],
                external_urls = d['external_urls']['spotify']
            )
            session.merge(src)
            all_albums.append(src)

        session.commit()
        print( '[  OK  ] Inserted {} Artists.'.format(len(all_artists )) )

        return all_artists 


class Artist_MBZ(Source):
    __tablename__ = 'musicbrainz_Artists'


class Artist_FS(Source):
    __tablename__ = 'filesystem_Artists'



class ArtistRef(Reference):
    __tablename__ = 'ref_Artists'

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
    ArtistRef.__table__.drop(engine)
    Artist_SPT.__table__.drop(engine)
    Artist_MBZ.__table__.drop(engine)
    Artist_FS.__table__.drop(engine)

    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)

    # Declare a common session for multiple files
    session = sessionmaker(bind=engine, autoflush=False)()

    h1 = session.query(Host).first()

    # Start of Data Insersions --------{
    import os, json
    cwd = os.path.split(os.path.realpath(__file__))[0]
    with open('{}/spotify/jsondumps-full/get_artist_related_artists.json'.format(os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )

    sources = Artist_SPT.add_sources(session, data)
    refs = ArtistRef.add_references(session, h1.id, sources)

    session.commit()
    session.close()
    #------- End of Data Submitting ---------


if __name__ == '__main__':
    pass
    main()



print('[  OK  ] IMPORTED: {}'.format(__name__))
