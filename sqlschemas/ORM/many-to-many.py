from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship


#------- Start of ORM Definitions ---------
Base = declarative_base()

radio_users = Table('radio_users', Base.metadata,
    Column('whatever_name1', Integer, ForeignKey('radios.id')),
    Column('whatever_name2', Integer, ForeignKey('users.id'))
)

class Radio(Base):
    __tablename__ = 'radios'

    rid = Column('id', Integer, primary_key=True)
    followers = relationship('User',
        secondary=radio_users,
        back_populates='subscriptions'
    )

class User(Base):
    __tablename__ = 'users'

    uid = Column('id', Integer, primary_key=True)
    subscriptions = relationship('Radio',
        secondary=radio_users,
        back_populates='followers'
    )


#------- End of ORM Definitions ---------


#------- Start of Data Insersions ---------
r1 = Radio()
r2 = Radio()
r3 = Radio()
u1 = User()
u2 = User()
u3 = User()

r1.followers.append(u1)
r1.followers.append(u2)
r1.followers.append(u3)

u1.subscriptions.append(r2)
u1.subscriptions.append(r3)
#------- End of Data Insersions ---------



#------- Start of Data Browsing ---------
for u in r1.followers:
    print('Radio"s follower: %s'%u)

for r in u1.subscriptions:
    print('User"s subscriptions: %s'%r)

#------- End of Data Browsing ---------



#------- Start of Data Submitting ---------

# Connect Database
engine = create_engine('sqlite:///test.sqlite', echo=False)

# Clearout all existing tables
Base.metadata.drop_all(engine)
#Radio.__table__.drop(engine)
#User.__table__.drop(engine)

# Let new Schemas take effect
Base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine)()

session.add(r1)
session.add(r2)
session.add(r3)
session.add(u1)
session.add(u2)
session.add(u3)

session.commit()
session.close()
#------- End of Data Submitting ---------


print('[  OK  ]')
