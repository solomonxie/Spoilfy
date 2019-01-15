from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

import uuid


#------- Start of ORM Definitions ---------
Base = declarative_base()


# ==============================================================
# >>>>>>>>>>>>>[    User Tables     ] >>>>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

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
    uid = Column('uid', Integer, ForeignKey('u_Users.uid'))
    ref_id = Column('ref_id', Integer, ForeignKey('ref_Tracks.ref_id'))
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

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String)

class Track_SPT(TrackSource):
    __tablename__ = 'spotify_Tracks'

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

    id = Column('id', Integer, primary_key=True)
    ref_id = Column('ref_id', String, nullable=False)  #>> unique reference ID
    host_id = Column('host_id', Integer, ForeignKey('hosts.id'))
    src_id = Column('src_id', String, nullable=False)  #>> dynamic | not speicify FK

    def addSource(TrackSource):
        pass



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


# 1. Add Hosts
h1 = Host(name='Spotify',
        tbname_track='spotify_Tracks',
        tbname_album='spotify_Albums',
        tbname_artist='spotify_Artists',
        tbname_playlist='spotify_Playlists'
)
h2 = Host(name='MusicBrainz',
        tbname_track='musicbrainz_Tracks',
        tbname_album='musicbrainz_Albums',
        tbname_artist='musicbrainz_Artists',
        tbname_playlist='musicbrainz_Playlists'
)
session.add_all([h1, h2])
session.flush()  # Generate data for Dynamic fileds(primary key) to get values

# 2. Add source tracks from Spotify
src1_1 = Track_SPT(title='139')
src1_2 = Track_SPT(title='Hey Jdue')
src1_3 = Track_SPT(title='Now is not a good time')
session.add_all([src1_1, src1_2, src1_3])

# 3. Add source tracks from MusicBrainz
src2_1 = Track_MBZ(title='139')
src2_2 = Track_MBZ(title='Hey Jude')
src2_3 = Track_MBZ(title='Now is not a good time')
session.add_all([src2_1, src2_2, src2_3])
session.flush()  # Generate data for Dynamic fileds(primary key) to get values

# 4. Initialize references
t1 = ref1 = TrackRef(ref_id=str(uuid.uuid1()), src_id=src1_1.id, host_id=h1.id)
t2 = ref2 = TrackRef(ref_id=str(uuid.uuid1()), src_id=src1_2.id, host_id=h1.id)
t3 = ref3 = TrackRef(ref_id=str(uuid.uuid1()), src_id=src1_3.id, host_id=h1.id)
session.add_all([ref1, ref2, ref3])
session.flush()  # Generate data for Dynamic fileds(primary key) to get values

# 5. Add references to existing tracks
ref4 = TrackRef(ref_id=t1.ref_id, src_id=src1_1.id, host_id=h2.id)
ref5 = TrackRef(ref_id=t2.ref_id, src_id=src1_2.id, host_id=h2.id)
ref6 = TrackRef(ref_id=t3.ref_id, src_id=src1_3.id, host_id=h2.id)
session.add_all([ref4, ref5, ref6])
session.flush()  # Generate data for Dynamic fileds(primary key) to get values

# 6. Add Users
u1 = User(name='Jason')
u2 = User(name='David')
u3 = User(name='Sol')
session.add_all([u1,u2,u3])
session.flush()  # Generate data for Dynamic fileds(primary key) to get values

# 6. Add User Tracks
ut1 = UserTrack(uid=u1.uid, ref_id=t1.ref_id)
ut2 = UserTrack(uid=u1.uid, ref_id=t2.ref_id)
ut3 = UserTrack(uid=u1.uid, ref_id=t3.ref_id)
session.add_all([ut1, ut2, ut3])
session.flush()

    # }------- End of Data Insersions


session.commit()
session.close()
#------- End of Data Submitting ---------


# Start of Data Browsing ---------{

"""
>>> SQL:

    SELECT
        tb1.tid, tb1.tid_spt, tb1.tid_mbz,
        tb2.title as "title_spt",
        tb3.title as "title_mbz"
    FROM
        "ref_Tracks" AS tb1
        INNER JOIN "spotify_Tracks" AS tb2 ON tb1.tid == tb2.tid
        INNER JOIN "musicbrainz_Tracks" AS tb3 ON tb1.tid == tb3.tid

"""

# Manually search multiple level relationship (many to many to many)
#u = session.query(User).first()
#print(u.name)
#for t in u.tracks:
#    if t.tid_spt:
#        t_spt = session.query(Track_SPT).filter(Track_SPT.tid == t.tid_spt).first()
#        if t_spt:
#            print('Track:%s'% t_spt.title)

#query = session.query(
#    User, UserTrack, Track, Track_SPT, Track_MBZ
#).filter(
#    User.uid == UserTrack.uid
#).filter(
#    UserTrack.tid == Track.tid
#).filter(
#    #Track.tid in [Track_SPT.tid, Track_MBZ.tid]
#    Track.tid == Track_SPT.tid or Track.tid == Track_MBZ.tid
#).group_by(
#    Track.tid
#).all()
#
#for u,ut,t,t_spt,t_mbz in query:
#    print(u.name, 'has track:', ut.tid, t_spt.title)
#

# }------- End of Data Browsing


print('[  OK  ]')
