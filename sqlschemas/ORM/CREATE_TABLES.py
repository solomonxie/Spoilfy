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
    title = Column('title', String)
    #tid_spt = Column('tid_spt', Integer, ForeignKey('spotify_Tracks.tid_spt'))
    #tid_mbz = Column('tid_mbz', Integer, ForeignKey('musicbrainz_Tracks.tid_mbz'))
    #tids_fs = Column('tids_fs', Sequence)

    users = relationship('User', secondary=user_tracks, back_populates='tracks')


class Track_MBZ(Base):
    __tablename__ = 'musicbrainz_Tracks'

    tid = Column('tid_mbz', Integer, primary_key=True)
    title = Column('title', Integer)


#------ Start of Data Insersions ---------
h1 = Host(name='Spotify')
h2 = Host(name='MusicBrainz')
h3 = Host(name='iTunes')

t1 = Track(title='139')
t2 = Track(title='Hey Jdue')
t3 = Track(title='Now is not a good time')

u1 = User(name='Jason', hosts=[h1,h2])
u1.tracks += [t1,t2,t3]

u2 = User(name='David', hosts=[h1,h3])
u3 = User(name='Sol', hosts=[h1,h2,h3])

#------- End of Data Insersions ---------



#------- Start of Data Browsing ---------
#------- End of Data Browsing ---------



#------- Start of Data Submitting ---------

# Connect Database
engine = create_engine('sqlite:///db_u_spoilfy.sqlite', echo=False)

# Clearout all existing tables
Base.metadata.drop_all(engine)
#Host.__table__.drop(engine)
#User.__table__.drop(engine)

# Let new Schemas take effect
Base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine)()

session.add(u1)
session.add(u2)
session.add(u3)

session.add(h1)
session.add(h2)
session.add(h3)

session.commit()
session.close()
#------- End of Data Submitting ---------


print('[  OK  ]')
