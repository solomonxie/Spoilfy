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

class User(Base):
    __tablename__ = 'u_Users'

    uid = Column('uid', Integer, primary_key=True)
    name = Column('name', String)

    hosts = relationship('Host', secondary=user_hosts, back_populates='users')
    #tracks = relationship('Track', secondary=user_tracks, back_populates='users')
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

#------- Start of Data Submitting ---------

# Connect Database
import os
cwd = os.path.split(os.path.realpath(__file__))[0]
engine = create_engine('sqlite:///{}/db_u_spoilfy.sqlite'.format(cwd), echo=False)

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

u1 = User(name='Jason', hosts=[h1,h2])
u2 = User(name='David', hosts=[h1,h3])
u3 = User(name='Sol', hosts=[h1,h2,h3])
session.add_all([u1,u2,u3])
session.flush()  # Generate data for Dynamic fileds(primary key) to get values

    # }------- End of Data Insersions


session.commit()
session.close()
#------- End of Data Submitting ---------


# Start of Data Browsing ---------{
# Manually search multiple level relationship (many to many to many)
u = session.query(User).first()
print(u.name)
for h in u.hosts:
    print('Host on: %s'% h.name)
# }------- End of Data Browsing


print('[  OK  ]')
