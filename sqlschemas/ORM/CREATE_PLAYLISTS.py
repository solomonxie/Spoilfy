import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence


#-------[  Import From Other Modules   ]---------
from common_base import Base, engine
from common_orms import Host, User, UserItem, Resource, Reference



# ==============================================================
# >>>>>>>>>>>>>[    Independent Tables     ] >>>>>>>>>>>>>>>>>>>
# ==============================================================


class Playlist_SPT(Resource):
    """ [ Playlist in Spotify ]
    :PKs : [id, name]
    """
    __tablename__ = 'spotify_Playlists'

    id = Column('id', String, primary_key=True)
    name = Column('name', String, primary_key=True)
    owner_id = Column('owner_id', String)
    snapshot_id = Column('snapshot_id', String)
    tids = Column('track_ids', String)

    total_tracks = Column('total_tracks', Integer)
    followers = Column('followers', Integer)
    collaborative = Column('collaborative', Boolean)
    description = Column('description', String)
    public = Column('public', Boolean)
    images = Column('images', String)
    uri = Column('uri', String)
    href = Column('href', String)
    external_urls = Column('external_urls', String)

    
    @classmethod
    def add(cls, session, jsondata):
        j = jsondata
        item = cls(
            id = j['id'],
            name = j['name'],
            owner_id = j['owner']['id'],
            snapshot_id = j['snapshot_id'],
            tids = str(j['tracks']['href']),
            total_tracks = j['tracks']['total'],
            followers = j['followers']['total'],
            public = j['public'],
            collaborative = j['collaborative'],
            description = j['description'],
            images = str(j['images']),
            uri = j['uri'],
            href = j['href'],
            external_urls = j['external_urls']['spotify'],
        )
        session.merge( item )   #Merge existing data
        #session.commit()  #-> Better to commit after multiple inserts
        return item



class Playlist_FS(Resource):
    __tablename__ = 'filesystem_playlists'





# =====================================================================
# >>>>>>>>>>>>>>>>>>[    User Table     ] >>>>>>>>>>>>>>>>>>>>>>>>>>>>
# =====================================================================



class UserPlaylist(UserItem):
    """[  User's favorite playlists  ]
    :PKs: [ref_id, uid]
    :field last_played: Last time played the playlist
    :field added_at: Time added to the source library
    :field rate: Personal rating to the playlist
    :field memo: Personal comments
    :staticmethod add_from_spotify: 
    """
    __tablename__ = 'u_Playlists'
    src_type = 'playlist'

    uid = Column('uid', String, ForeignKey('u_Users.uid'), primary_key=True)
    ref_id = Column('ref_id', String, ForeignKey('references.ref_id'), primary_key=True)

    last_played = Column('last_played', String)
    added_at = Column('added_at', String)
    count = Column('count', Integer)
    rate = Column('rate', Integer)
    memo = Column('memo', String)

    @classmethod
    def add_items(cls, session, host_id, uid, jsondata, srcClass):
        """ [ add batch items ]
        :param {jsondata} List type:
        :param {srcClass} Resource class type:
        """
        user_items = []
        for playlist in jsondata:
            data = cls.get_playlist_tracks(playlist['id'])
            src = srcClass.add(session, data)
            ref = Reference.add(session, cls.src_type, host_id, src.id)
            uitem = cls.add(session, uid, ref.ref_id, data)

            user_items.append( uitem )
            #-> Temp: commit here for test only to solve reeated ID issue.
            session.commit()

        session.commit()
        print('[  OK  ] Inserted {} User {}s.'.format(
            len(user_items), cls.src_type
        ))
        return user_items

    @classmethod
    def add(cls, session, uid, ref_id, jsondata):
        item = cls(
            uid = uid,
            ref_id = ref_id,
            last_played = None,
            count = 0,
            rate = 0,
            memo = ''
        )
        session.merge( item )
        #session.commit()  #-> Better to commit after multiple inserts
        return item

    @classmethod
    def get_playlist_tracks(cls, playlist_id):
        """ [ Get playlist tracks ]
        """
        import os, json
        cwd = os.path.split(os.path.realpath(__file__))[0]
        with open('{}/spotify/jsondumps-full/get_playlist.json'.format(os.path.dirname(cwd)), 'r') as f:
            data = json.loads( f.read() )
        return data







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
        Playlist_SPT.__table__.drop(engine)
        Playlist_FS.__table__.drop(engine)
        UserPlaylist.__table__.drop(engine)
    except Exception as e:
        print('Error on dropping Playlist tables.')

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
    # Add User playlists
    with open('{}/spotify/jsondumps-full/get_user_playlists.json'.format(os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )
    UserPlaylist.add_items(
        session, h1.id, user.uid,
        data['items'], Playlist_SPT
    )

    # Get next page
    next_url = data['next']
    # }------- End of Data Insersions


    session.commit()
    session.close()
    #------- End of Data Submitting ---------


if __name__ == '__main__':
    main()



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
