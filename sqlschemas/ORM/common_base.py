from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

import os


# Declare a common base for multiple files
Base = declarative_base()

# Connect Database
cwd = os.path.split(os.path.realpath(__file__))[0]
engine = create_engine('sqlite:///{}/db_u_spoilfy.sqlite'.format(cwd), echo=False)

print('[  OK  ] IMPORTED: {}'.format(__name__))
