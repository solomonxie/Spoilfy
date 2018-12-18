import uuid

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence


#-------[  Import From Other Modules   ]---------
from common_base import Base, engine, session



# ==============================================================
# >>>>>>>>>>>>>[    Independent Tables     ] >>>>>>>>>>>>>>>>>>>
# ==============================================================

class Host(Base):
    """
    :field host_type: [MediaProvider, InfoProvider, FileSystem]
    :field uri: API entry point.
    :field tbname_*: Related table names in database
    """
    __tablename__ = 'hosts'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    host_type = Column('type', String)
    uri = Column('URI', String)
    info = Column('info', String)

    tbname_track = Column('tbname_track', String)
    tbname_album = Column('tbname_album', String)
    tbname_artist = Column('tbname_artist', String)
    tbname_playlist = Column('tbname_playlist', String)



# ==============================================================
# >>>>>>>>>>>>>>>>>>>[    METHODS     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


def add_hosts(session, jsondata):
    all_hosts = []
    for h in jsondata['hosts']:
        host = Host(
            name=h['name'],
            host_type=h['type'],
            uri=h['uri'],
            info=h['info'],
            tbname_track=h['tbname_track'],
            tbname_album=h['tbname_album'],
            tbname_artist=h['tbname_artist'],
            tbname_playlist=h['tbname_playlist']
        )
        session.merge(host)
        all_hosts.append(host)

    session.commit()
    print( '[  OK  ] Inserted {} hosts.'.format(len(all_hosts)) )

    return all_hosts



# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


def main():
    #------- Start of Data Submitting ---------
    # Clearout all existing tables
    Base.metadata.drop_all(engine)

    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)

    import os, json
    cwd = os.path.split(os.path.realpath(__file__))[0]
    with open('{}/hosts.json'.format(os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )
        add_hosts(session, data)

    # Start of Data Insersions --------{
    #h1 = Host(name='Spotify',
    #        tbname_track='spotify_Tracks',
    #        tbname_album='spotify_Albums',
    #        tbname_artist='spotify_Artists',
    #        tbname_playlist='spotify_Playlists'
    #)
    #h2 = Host(name='MusicBrainz',
    #        tbname_track='musicbrainz_Tracks',
    #        tbname_album='musicbrainz_Albums',
    #        tbname_artist='musicbrainz_Artists',
    #        tbname_playlist='musicbrainz_Playlists'
    #)
    #session.add_all([h1, h2])
    # }------- End of Data Insersions


    session.commit()
    session.close()
    #------- End of Data Submitting ---------



if __name__ == '__main__':
    main()



print('[  OK  ] IMPORTED: {}'.format(__name__))
