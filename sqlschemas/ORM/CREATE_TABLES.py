from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship


#------- Start of ORM Definitions ---------
Base = declarative_base()

user_hosts = Table('u_Hosts', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('uid', Integer, ForeignKey('u_Users.uid')),
    Column('host_id', Integer, ForeignKey('hosts.host_id')),
    Column('uid_on_host', Integer),
    Column('auth', String),
    Column('name', String),
    Column('nickname', String),
    Column('email', String),
    Column('info', String),
)

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

class User(Base):
    __tablename__ = 'u_Users'

    uid = Column('uid', Integer, primary_key=True)
    name = Column('name', String)

    hosts = relationship('Host', secondary=user_hosts, back_populates='users')
    tracks = relationship('Track', secondary=user_tracks, back_populates='users')
    #albums = relationship('Album', secondary=user_albums, back_populates='users')
    #artists = relationship('Artist', secondary=user_artists, back_populates='users')
    #playlists = relationship('Playlist', secondary=user_playlists, back_populates='users')


class Host(Base):
    __tablename__ = 'hosts'

    hid = Column('host_id', Integer, primary_key=True)
    name = Column('name', String)
    uri = Column('URI', String)
    auths = Column('auth_methods', String)
    info = Column('info', String)

    users = relationship('User', secondary=user_hosts, back_populates='hosts')


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
engine = create_engine('sqlite:///db_u_spoilfy.sqlite', echo=False)

# Clearout all existing tables
Base.metadata.drop_all(engine)
#Host.__table__.drop(engine)
#User.__table__.drop(engine)

# Let new Schemas take effect
Base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine, autoflush=False)()

    # Start of Data Insersions --------{

h1 = Host(name='Spotify')
h2 = Host(name='MusicBrainz')
h3 = Host(name='iTunes')
session.add_all([h1, h2, h3])
session.flush()  # Flush data for Dynamic Fileds to get their IDs

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

# Add User tracks with connection to multiple Source Libraries
t1 = Track(tid_spt=src1_1.tid, tid_mbz=src2_1.tid)
t2 = Track(tid_spt=src1_2.tid, tid_mbz=src2_2.tid)
t3 = Track(tid_spt=src1_3.tid, tid_mbz=src2_3.tid)
session.add_all([t1, t2, t3])
session.flush()  # Generate data for Dynamic fileds(primary key) to get values

u1 = User(name='Jason', hosts=[h1,h2], tracks=[t1,t2,t3])
u2 = User(name='David', hosts=[h1,h3], tracks=[t1,t2])
u3 = User(name='Sol', hosts=[h1,h2,h3], tracks=[t1,t3])
session.add_all([u1,u2,u3])
session.flush()  # Generate data for Dynamic fileds(primary key) to get values

    # }------- End of Data Insersions


session.commit()
session.close()
#------- End of Data Submitting ---------


# Start of Data Browsing ---------{
u = session.query(User).first()
print(u.name)
for t in u.tracks:
    if t.tid_spt:
        t_spt = session.query(Track_SPT).filter(Track_SPT.tid == t.tid_spt).first()
        if t_spt:
            print('Track:%s'% t_spt.title)
# }------- End of Data Browsing


print('[  OK  ]')
