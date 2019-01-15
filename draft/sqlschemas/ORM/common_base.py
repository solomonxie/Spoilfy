import uuid

#-------[  Import SQLAlchemy ]---------
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence


# Declare a common base for multiple files
Base = declarative_base()

# Connect Database
engine = create_engine('sqlite:////tmp/db_u_spoilfy.sqlite', echo=False)



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
