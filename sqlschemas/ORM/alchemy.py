

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///test.sqlite', echo=True)
Base = declarative_base()

class Father(Base):
    __tablename__ = 'father'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)


class Child(Base):
    __tablename__ = 'child'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    #father_id = Column(Integer, ForeignKey('father.id'))


Base.metadata.create_all(bind=engine)





def insert_data():
    session = sessionmaker(bind=engine)()

    daddy = Father(name='David')
    jason = Child(name='Jason')
    emma = Child(name='Emma')
    
    session.add(daddy)
    session.add(jason)
    session.add(emma)
    session.commit()

#insert_data()


