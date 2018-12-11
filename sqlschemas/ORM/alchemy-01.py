

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

Base = declarative_base()

class Father(Base):
    __tablename__ = 'father'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)

    children = relationship('Child')


class Child(Base):
    __tablename__ = 'child'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    father_id = Column(Integer, ForeignKey('father.id'))

daddy = Father()
jason = Child()
emma = Child()

daddy.children.append(jason)
daddy.children.append(emma)

print( daddy.children )


