from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship


#------- Start of ORM Definitions ---------
Base = declarative_base()

class One(Base):
    __tablename__ = 'one'

    oid = Column('id', Integer, primary_key=True)
    children = relationship('Many', back_populates='parent')

class Many(Base):
    __tablename__ = 'many'

    mid = Column('id', Integer, primary_key=True)
    one_id = Column(Integer, ForeignKey('one.id'))
    parent = relationship('One', back_populates='children')


# Connect Database
engine = create_engine('sqlite:///test.sqlite', echo=False)
# Clearout all existing tables
Base.metadata.drop_all(engine)
#One.__table__.drop(engine)
#Many.__table__.drop(engine)
# Let new Schemas take effect
Base.metadata.create_all(bind=engine)
#------- End of ORM Definitions ---------


#------- Start of Data Insersions ---------
daddy = One()
jason = Many(parent=daddy)
emma = Many(parent=daddy)
#------- End of Data Insersions ---------



#------- Start of Data Browsing ---------
for c in daddy.children:
    print( 'Children"s daddy: %s'%c.parent )
#------- End of Data Browsing ---------



#------- Start of Data Submitting ---------
session = sessionmaker(bind=engine)()
session.add(daddy)
session.add(jason)
session.add(emma)
session.commit()
session.close()
#------- End of Data Submitting ---------


print('[  OK  ]')
