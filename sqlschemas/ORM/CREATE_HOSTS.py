import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence


#-------[  Import From Other Modules   ]---------
from common_base import Base, engine



# ==============================================================
# >>>>>>>>>>>>>[    Independent Tables     ] >>>>>>>>>>>>>>>>>>>
# ==============================================================




class Host(Base):
    """ [ Music Information Host Providers ]
    :KEY host_type: [MediaProvider, InfoProvider, FileSystem]
    :KEY uri: API entry point.
    :KEY tbname_*: Related table names in database
    :Note : 
        Host class is an 'origin' class & can't be treated as a resource
        If not so, it'll cause Loop Import problem.
    """
    __tablename__ = 'hosts'

    id = Column('id', String, primary_key=True)
    name = Column('name', String)

    host_type = Column('type', String)
    uri = Column('URI', String)
    info = Column('info', String)

    tbname_track = Column('tbname_track', String)
    tbname_album = Column('tbname_album', String)
    tbname_artist = Column('tbname_artist', String)
    tbname_playlist = Column('tbname_playlist', String)

    @classmethod
    def add_sources(cls, session, jsonItems):
        """[ Add Resources ]
        :param session: SQLAlchemy session object connected to DB
        :param String jsondump: JSON data in string format
        :return: Class instances of track resources
        """
        all_items = []
        for j in jsonItems:
            item = cls.add(session, j)
            all_items.append( item )

        session.commit()
        print('[  OK  ] Inserted {} items to [{}].'.format(
            len(all_items), cls.__tablename__
        ))

        return all_items

    @classmethod
    def add(cls, session, jsondata):
        j = jsondata
        item = cls(
            id=str(uuid.uuid1()),
            name=j['name'],
            host_type=j['type'],
            uri=j['uri'],
            info=j['info'],
            tbname_track=j['tbname_track'],
            tbname_album=j['tbname_album'],
            tbname_artist=j['tbname_artist'],
            tbname_playlist=j['tbname_playlist']
        )
        session.merge( item )   #Merge existing data
        #session.commit()  #-> Better to commit after multiple inserts

        return item



# ==============================================================
# >>>>>>>>>>>>>>>>>>>[    METHODS     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================




# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


def main():
    #------- Start of Data Submitting ---------
    # Clearout all existing tables
    try:
        Host.__table__.drop(engine)
    except Exception as e:
        print('Error on dropping Host table.')

    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)

    # Declare a common session for multiple files
    session = sessionmaker(bind=engine, autoflush=False)()

    # Start of Data Insersions --------{
    import os, json
    cwd = os.path.split(os.path.realpath(__file__))[0]
    with open('{}/hosts.json'.format(os.path.dirname(cwd)), 'r') as f:
        data = json.loads( f.read() )

    hosts = Host.add_sources(session, data['hosts'])
    # }------- End of Data Insersions

    session.commit()
    session.close()
    #------- End of Data Submitting ---------



if __name__ == '__main__':
    main()



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
