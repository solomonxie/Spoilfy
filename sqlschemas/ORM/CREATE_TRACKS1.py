from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

"""
SQL:
    SELECT
        tb1.tid, tb1.tid_spt, tb1.tid_mbz,
        tb2.title as "title_spt",
        tb3.title as "title_mbz"
    FROM
        "ref_Tracks" AS tb1
        INNER JOIN "spotify_Tracks" AS tb2 ON tb1.tid == tb2.tid
        INNER JOIN "musicbrainz_Tracks" AS tb3 ON tb1.tid == tb3.tid
"""

#------- Start of ORM Definitions ---------
Base = declarative_base()

user_tracks = Table('u_Tracks', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('uid', Integer, ForeignKey('u_Users.uid')),
    Column('tid', Integer, ForeignKey('ref_Tracks.tid')),
    Column('last_played', Date),
    Column('added_at', Date),
    Column('count', Integer),
    Column('rate', Integer),
    Column('memo', String)
)

class UserTracks(Base):
    __tablename__ = 'usertracks'

    utid = Column('utid', Integer, primary_key=True)
    uid = Column('uid', Integer, ForeignKey('u_Users.uid'))
    tid = Column('tid', Integer, ForeignKey('ref_Tracks.tid'))
    last_played = Column('last_played', Date)
    added_at = Column('added_at', Date)
    count = Column('count', Integer)
    rate = Column('rate', Integer)
    memo = Column('memo', String)

class User(Base):
    __tablename__ = 'u_Users'

    uid = Column('uid', Integer, primary_key=True)
    name = Column('name', String)

    tracks = relationship('Track', secondary=user_tracks, back_populates='users')
    #albums = relationship('Album', secondary=user_albums, back_populates='users')
    #artists = relationship('Artist', secondary=user_artists, back_populates='users')
    #playlists = relationship('Playlist', secondary=user_playlists, back_populates='users')

class Track(Base):
    __tablename__ = 'ref_Tracks'

    tid = Column('tid', Integer, primary_key=True)
    tid_spt = Column('tid_spt', Integer, ForeignKey('spotify_Tracks.tid'))
    tid_mbz = Column('tid_mbz', Integer, ForeignKey('musicbrainz_Tracks.tid'))
    #tids_fs = Column('tids_fs', Sequence)

    users = relationship('User', secondary=user_tracks, back_populates='tracks')


class Track_SPT(Base):
    """
    Independent table, without any setup to relate User tables
    Manually search by id if needed.
    """
    __tablename__ = 'spotify_Tracks'

    tid = Column('tid', Integer, primary_key=True)
    title = Column('title', String)


class Track_MBZ(Base):
    """
    Independent table, without any setup to relate User tables
    Manually search by id if needed.
    """
    __tablename__ = 'musicbrainz_Tracks'

    tid = Column('tid', Integer, primary_key=True)
    title = Column('title', Integer)



#------- Start of Data Submitting ---------

# Connect Database
import os
cwd = os.path.split(os.path.realpath(__file__))[0]
engine = create_engine('sqlite:///{}/db_u_spoilfy.sqlite'.format(cwd), echo=True)


# Clearout all existing tables
Base.metadata.drop_all(engine)

# Let new Schemas take effect
Base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine, autoflush=False)()

    # Start of Data Insersions --------{

# Add Users
u1 = User(name='Jason')
u2 = User(name='David')
u3 = User(name='Sol')
session.add_all([u1,u2,u3])
session.flush()  # Generate data for Dynamic fileds(primary key) to get values

# Add source tracks in Spotify's Library
src1_1 = Track_SPT(title='139')
src1_2 = Track_SPT(title='Hey Jdue')
src1_3 = Track_SPT(title='Now is not a good time')
session.add_all([src1_1, src1_2, src1_3])

# Add source tracks in MusicBrainz's Library
src2_1 = Track_MBZ(title='139')
src2_2 = Track_MBZ(title='Hey Jude')
src2_3 = Track_MBZ(title='Now is not a good time')
session.add_all([src2_1, src2_2, src2_3])
session.flush()  # Generate data for Dynamic fileds(primary key) to get values

# Add Reference tracks with connection to multiple Source Libraries
t1 = Track(tid_spt=src1_1.tid, tid_mbz=src2_1.tid)
t2 = Track(tid_spt=src1_2.tid, tid_mbz=src2_2.tid)
t3 = Track(tid_spt=src1_3.tid, tid_mbz=src2_3.tid)
u1.tracks += [t1,t2,t3]
u2.tracks += [t1,t3]
u3.tracks += [t2,t3]
session.add_all([t1, t2, t3])
session.flush()  # Generate data for Dynamic fileds(primary key) to get values

# Add User Tracks
ut1 = UserTracks(uid=u1.uid, tid=t1.tid)
ut2 = UserTracks(uid=u1.uid, tid=t2.tid)
ut3 = UserTracks(uid=u1.uid, tid=t3.tid)
session.add_all([ut1, ut2, ut3])
session.flush()

    # }------- End of Data Insersions


session.commit()
session.close()
#------- End of Data Submitting ---------


# Start of Data Browsing ---------{
# Manually search multiple level relationship (many to many to many)
#u = session.query(User).first()
#print(u.name)
#for t in u.tracks:
#    if t.tid_spt:
#        t_spt = session.query(Track_SPT).filter(Track_SPT.tid == t.tid_spt).first()
#        if t_spt:
#            print('Track:%s'% t_spt.title)

query = session.query(
    User, UserTracks, Track, Track_SPT, Track_MBZ
).filter(
    User.uid == UserTracks.uid
).filter(
    UserTracks.tid == Track.tid
).filter(
    #Track.tid in [Track_SPT.tid, Track_MBZ.tid]
    Track.tid == Track_SPT.tid or Track.tid == Track_MBZ.tid
).group_by(
    Track.tid
).all()

for u,ut,t,t_spt,t_mbz in query:
    print(u.name, 'has track:', ut.tid, t_spt.title)


# }------- End of Data Browsing


print('[  OK  ]')
