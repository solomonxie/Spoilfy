import uuid
from datetime import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence


#-------[  Import From Other Modules   ]---------
from common_base import Base, engine
from common_orms import Host, User, UserItem, Resource, Reference



# ==============================================================
# >>>>>>>>>>>>>[    Independent Tables     ] >>>>>>>>>>>>>>>>>>>
# ==============================================================



class Artist_SPT(Resource):
    __tablename__ = 'spotify_Artists'

    genres = Column('genres', String)
    followers = Column('followers', Integer)
    popularity = Column('popularity', Integer)
    uri = Column('uri', String)
    href = Column('href', String)
    external_urls = Column('external_urls', String)


    @classmethod
    def add(cls, session, jsondata):
        d = jsondata
        item = cls(
            id = d['id'],
            name = d['name'],
            genres = str(d['genres']),
            followers = d['followers']['total'],
            popularity = d['popularity'],
            uri = d['uri'],
            href = d['href'],
            external_urls = str(d['external_urls'])
        )
        session.merge( item )   #Merge existing data
        #session.commit()  #-> Better to commit after multiple inserts
        return item


class Artist_MBZ(Resource):
    __tablename__ = 'musicbrainz_Artists'


class Artist_FS(Resource):
    __tablename__ = 'filesystem_Artists'





# =====================================================================
# >>>>>>>>>>>>>>>>>>[    User Table     ] >>>>>>>>>>>>>>>>>>>>>>>>>>>>
# =====================================================================



class UserArtist(UserItem):
    """ [  User's followed artists ]
    :PKs: [ref_id, uid]
    :field rate: Personal rating to the album
    :field memo: Personal comments
    :staticmethod :
    """
    __tablename__ = 'u_Artists'
    src_type = 'artist'


    uid = Column('uid', String, ForeignKey('u_Users.uid'), primary_key=True)
    ref_id = Column('ref_id', String, ForeignKey('references.ref_id'), primary_key=True)

    memo = Column('memo', String)

    @classmethod
    def add(cls, session, uid, ref_id, jsondata):
        item = cls(
            uid = uid,
            ref_id = ref_id,
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
        Artist_SPT.__table__.drop(engine)
        Artist_MBZ.__table__.drop(engine)
        Artist_FS.__table__.drop(engine)
        UserArtist.__table__.drop(engine)
    except Exception as e:
        print('Error on dropping Artist tables.')


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
    with open('{}/spotify/jsondumps-full/get_user_artists.json'.format(os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )

    next_url = data['artists']['next']

    # Add user artists
    UserArtist.add_items(
        session, h1.id, user.uid,
        data['artists']['items'], Artist_SPT
    )

    session.commit()
    session.close()
    #------- End of Data Submitting ---------


if __name__ == '__main__':
    main()



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
