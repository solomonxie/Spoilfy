import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence


#-------[  Import From Other Modules   ]---------
from common_base import Base, engine
from common_orms import Host, User, UserItem, Resource, Reference



# ==============================================================
# >>>>>>>>>>>>>[    Independent Tables     ] >>>>>>>>>>>>>>>>>>>
# ==============================================================



class Album_SPT(Resource):
    __tablename__ = 'spotify_Albums'

    atids = Column('artist_ids', String)
    tids = Column('track_ids', String)

    release_date = Column('release_date', String)
    release_date_precision = Column('release_date_precision', String)
    total_tracks = Column('total_tracks', Integer)
    lable = Column('lable', String)
    popularity = Column('popularity', Integer)
    copyrights = Column('copyrights', String)
    album_type = Column('album_type', String)
    uri = Column('uri', String)
    href = Column('href', String)
    external_urls = Column('external_urls', String)
    external_ids = Column('external_ids', String)

    #tracks = Column('tracks', String)  #>>For [Track_SPT]
    #artists = Column('artists', String)  #>>For [Artist_SPT]


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
        #session.commit()  #-> Better to commit after multiple inserts
        return item


class Album_MBZ(Resource):
    __tablename__ = 'musicbrainz_Albums'


class Album_FS(Resource):
    __tablename__ = 'filesystem_Albums'





# =====================================================================
# >>>>>>>>>>>>>>>>>>[    User Table     ] >>>>>>>>>>>>>>>>>>>>>>>>>>>>
# =====================================================================



class UserAlbum(UserItem):
    """ [  User's saved albums  ]
    :PKs: [ref_id, uid]
    :field last_played: Last time played the album
    :field added_at: Time added to the source library
    :field rate: Personal rating to the album
    :field memo: Personal comments
    :staticmethod :
    """
    __tablename__ = 'u_Albums'
    src_type = 'album'

    uid = Column('uid', String, ForeignKey('u_Users.uid'), primary_key=True)
    ref_id = Column('ref_id', String, ForeignKey('references.ref_id'), primary_key=True)

    added_at = Column('added_at', String)
    count = Column('count', Integer)
    rate = Column('rate', Integer)
    memo = Column('memo', String)

    @classmethod
    def add(cls, session, uid, ref_id, jsondata):
        item = cls(
            uid = uid,
            ref_id = ref_id,
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
        Album_SPT.__table__.drop(engine)
        Album_MBZ.__table__.drop(engine)
        Album_FS.__table__.drop(engine)
        UserAlbum.__table__.drop(engine)
    except Exception as e:
        print('Error on dropping Album tables.')

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
    with open('{}/spotify/jsondumps-full/get_user_albums.json'.format(os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )

    # Add user albums
    UserAlbum.add_items(
        session, h1.id, user.uid,
        data['items'], Album_SPT
    )

    session.commit()
    session.close()
    #------- End of Data Submitting ---------


if __name__ == '__main__':
    pass
    main()



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
