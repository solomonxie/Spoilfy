from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

import uuid


#------- Start of ORM Definitions ---------
Base = declarative_base()


# =====================================================================
# >>>>>>>>>>>>>>>>>>[    User Tables     ] >>>>>>>>>>>>>>>>>>>>>>>>>>>>
# =====================================================================

class User(Base):
    __tablename__ = 'u_Users'

    uid = Column('uid', Integer, primary_key=True)
    name = Column('name', String)

    def addTracks(self, sources=[]):
        pass


class UserHost(Base):
    __tablename__ = 'u_Hosts'

    id = Column('id', Integer, primary_key=True)
    uid = Column('uid', Integer, ForeignKey('u_Users.uid'))
    host_id = Column('host_id', Integer, ForeignKey('hosts.id'))
    uid_on_host = Column('uid_on_host', Integer)
    auth = Column('auth', String)
    name = Column('name', String)
    nickname = Column('nickname', String)
    email = Column('email', String)
    info = Column('info', String)


class UserTrack(Base):
    __tablename__ = 'u_Tracks'

    id = Column('id', Integer, primary_key=True)
    uid = Column('uid', String, ForeignKey('u_Users.uid'))
    ref_id = Column('ref_id', String, ForeignKey('ref_Tracks.ref_id'))
    last_played = Column('last_played', Date)
    added_at = Column('added_at', Date)
    count = Column('count', Integer)
    rate = Column('rate', Integer)
    memo = Column('memo', String)

    #def __init__(self, uid, src):
    #    self.uid = uid

    def addSource(self, src):
        """
            1. Check if source EXISTS in Track Reference Table
            2. If exists, get the "tid",
            3. If not, Insert new data to TrackRef, and get the "tid".
        """
        pass



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



#------- Start of Data Submitting ---------

# Connect Database
import os
cwd = os.path.split(os.path.realpath(__file__))[0]
engine = create_engine('sqlite:///{}/db_u_spoilfy.sqlite'.format(cwd), echo=False)


# Clearout all existing tables
Base.metadata.drop_all(engine)

# Let new Schemas take effect
Base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine, autoflush=False)()


    # Start of Data Insersions --------{

"""
>>> MRO:

    Jason = User('Jason')
    Jason.addTracks(data)
        |
        data = Track_MBZ.loadJSON('MusicBrainz-API-tracks.json')
            |....
        data = Track_SPT.loadJSON('spotify-API-tracks.json')
            |
            Track_SPT.addTracks()
                |
                TrackRef.addReference()
                    |
                    Host.checkHostForTrack()
            |
            return [Track_SPT]
        |
        UserTracks.addTrack( data[i].id )

"""


    # }------- End of Data Insersions


session.commit()
session.close()
#------- End of Data Submitting ---------




print('[  OK  ] {}'.format(__name__))
