import uuid

#-------[  Import SQLAlchemy ]---------
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence


# Declare a common base for multiple files
Base = declarative_base()

# Connect Database
engine = create_engine('sqlite:////tmp/db_spoilfy_uri.sqlite', echo=False)



# ==============================================================
# >>>>>>>>>>>>>>>>>>[    Abstract ORMs     ] >>>>>>>>>>>>>>>>>>>
# ==============================================================

class Resource(Base):
    """ [ Abstract ORM class ]
        Independent table, without any setup to relate User tables
        Manually search by id if needed.
    """
    __abstract__ = True

    uri = Column('uri', String, primary_key=True)
    name = Column('name', String)

    @classmethod
    def add_resource(cls, session, item):
        print('[TO BE IMPLEMENTED].')

    @classmethod
    def add_resources(cls, session, items):
        """[ Add Resources ]
        :param session: sqlalchemy SESSION binded to DB.
        :param LIST items: must be iteratable.
        :return: inserted resource objects.
        """
        all = []
        for j in items:
            item = cls.add(session, j)
            all_items.append( item )

        session.commit()
        print('[  OK  ] Inserted {} items to [{}].'.format(
            len(all), cls.__tablename__
        ))

        return all




class Reference(Base):
    """ [ References to map resources from different providers ]
        It maps things with SAME type but at different places.
    :KEY ref_id: as the REAL EXISTENCE of a resource.
    :KEY uri: refer to the target resource.
    """
    #__abstract__ = True
    __tablename__ = 'references'

    ref_id = Column('ref_id', String, primary_key=True)
    uri = Column('uri', String)

    @classmethod
    def add_ref(cls, session, uri, ref_id=None):
        ref = cls(
            uri = uri,
            ref_id = ref_id if ref_id else str(uuid.uuid1().hex)
        )
        session.merge(ref)
        #session.commit()  #-> Better to commit after multiple inserts
        return ref

    @classmethod
    def add_refs(cls, session, ref_items):
        """ [ Add batch references ]
        This method is called when:
          - It's already known which refers to which.
          - The "ref_items" has to be stricly in the format of
            [('uri', 'ref_id'), ('uri', 'ref_id'), ....]
        """
        all = []
        for pair in refs:
            ref = cls.add(session, pair[0], pair[1])
            all.append(ref)
        session.commit()
        print('[  OK  ] Inserted {} references.'.format(
            len(all)
        ))
        return all




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
        #User.__table__.drop(engine)
        pass
    except Exception as e:
        print('Error on dropping User table.')

    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)

    # Declare a common session for multiple files
    session = sessionmaker(bind=engine, autoflush=False)()


    # Start of Data Insersions --------{

    #import os, json
    #cwd = os.path.split(os.path.realpath(__file__))[0]
    ## Add Hosts
    #with open('{}/hosts.json'.format(os.path.dirname(cwd)), 'r') as f:
    #    data = json.loads( f.read() )
    #hosts = Host.add_sources(session, data['hosts'])
    ## Add a User
    #h1 = session.query(Host).first()
    #with open('{}/spotify/jsondumps-full/get_user_profile.json'.format(os.path.dirname(cwd)), 'r') as f:
    #    data = json.loads( f.read() )

    #User.add(session, h1.id, data)

    # }------- End of Data Insersions

    session.commit()
    session.close()
    #------- End of Data Submitting ---------



if __name__ == '__main__':
    main()



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
