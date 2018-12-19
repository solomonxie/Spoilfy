import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence


#-------[  Import From Other Modules   ]---------
from common_base import Base, engine
from CREATE_HOSTS import Host


# =====================================================================
# >>>>>>>>>>>>>>>>>>[    User Tables     ] >>>>>>>>>>>>>>>>>>>>>>>>>>>>
# =====================================================================


class User(Base):
    """ [  Store User's Private Data  ]
    :primary keys: [uid, host_id, user_id]
    :field uid: Unique UserID in current database
    :field host_id: 
    :field user_id: UserID on specific Host site
    """
    __tablename__ = 'u_Users'

    uid = Column('uid', String, primary_key=True)
    host_id = Column('host_id', Integer,
        ForeignKey('hosts.id'), primary_key=True
    )
    user_id = Column('user_id', String, primary_key=True)
    name = Column('name', String)
    external_urls = Column('external_urls', String)
    followers = Column('followers', Integer, default=0)
    href = Column('href', String)
    images = Column('images', String)
    user_type = Column('type', String)
    uri = Column('uri', String)

    @staticmethod
    def add(session, host_id, jsondata):
        user = User(
            uid = str(uuid.uuid1()),
            host_id = host_id,
            user_id = jsondata['id'],
            name = jsondata['display_name'],
            external_urls = jsondata['external_urls']['spotify'],
            followers = jsondata['followers']['total'],
            href = jsondata['href'],
            images = str(jsondata['images']),
            user_type = jsondata['type'],
            uri = jsondata['uri']
        )
        session.merge(user)
        session.commit()
        print( '[  OK  ] Inserted User: {}.'.format(user.name) )

        return user



# ==============================================================
# >>>>>>>>>>>>>>>>>>>[    METHODS     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


def main():
    #------- Start of Data Submitting ---------

    # Clearout all existing tables
    User.__table__.drop(engine)

    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)

    # Declare a common session for multiple files
    session = sessionmaker(bind=engine, autoflush=False)()

    h1 = session.query(Host).first()

    import os, json
    cwd = os.path.split(os.path.realpath(__file__))[0]
    with open('{}/spotify/jsondumps-full/get_user_profile.json'.format(os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )

    User.add(session, h1.id, data)

    # Start of Data Insersions --------{
    #u1 = User(name='Jason')
    #u2 = User(name='David')
    #u3 = User(name='Sol')
    #session.add_all([u1,u2,u3])
    #session.flush()  # Generate data for Dynamic fileds(primary key) to get values
    # }------- End of Data Insersions

    session.commit()
    session.close()
    #------- End of Data Submitting ---------



if __name__ == '__main__':
    main()



print('[  OK  ] IMPORTED: {}'.format(__name__))
