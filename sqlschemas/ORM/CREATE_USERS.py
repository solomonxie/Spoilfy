import uuid

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence


#-------[  Import From Other Modules   ]---------
from common_base import Base, engine, session


# =====================================================================
# >>>>>>>>>>>>>>>>>>[    User Tables     ] >>>>>>>>>>>>>>>>>>>>>>>>>>>>
# =====================================================================


class User(Base):
    __tablename__ = 'u_Users'

    uid = Column('uid', Integer, primary_key=True)
    name = Column('name', String)
    external_urls = Column('external_urls', String)
    followers = Column('followers', Integer, default=0)
    href = Column('href', String)
    images = Column('images', String)
    user_type = Column('type', String)
    uri = Column('uri', String)



# ==============================================================
# >>>>>>>>>>>>>>>>>>>[    METHODS     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


def add_user(session, jsondata):
    user = User(
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
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


def main():
    #------- Start of Data Submitting ---------

    # Clearout all existing tables
    Base.metadata.drop_all(engine)

    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)


    import os, json
    cwd = os.path.split(os.path.realpath(__file__))[0]
    with open('{}/spotify/jsondumps-full/get_user_profile.json'.format(os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )
        add_user(session, data)

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
