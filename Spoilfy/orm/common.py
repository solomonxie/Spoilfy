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

    #-> These 3 fields are included in URI
    id = Column('id', String)
    type = Column('type', String)
    provider = Column('provider', String)

    @classmethod
    def add(cls, session, data):
        print('[TO BE IMPLEMENTED].')

    @classmethod
    def add_resources(cls, session, items):
        """[ Add Resources ]
        :param session: sqlalchemy SESSION binded to DB.
        :param LIST items: must be iteratable.
        :return: inserted resource objects.
        """
        all = []
        for item in items:
            data = cls.get_sub_data(item)
            item = cls.add(session, data)
            all.append( item )

        session.commit()
        print('[  OK  ] Inserted {} items to [{}].'.format(
            len(all), cls.__tablename__
        ))

        return all

    @classmethod
    def get_sub_data(cls, item):
        """ [ Get sub item's data through Web API  ]
            This should retrive WebAPI accordingly
            This is to impelemented by children class.
        """
        return item



# ==============================================================
# >>>>>>>>>>>>>>>>[    COMMON ORMs     ] >>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


class Reference(Base):
    """ [ References to map resources from different providers ]
        It maps things with SAME type but at different places.
    :PK uri: refer to the target resource.
    :KEY real_uri: as the REAL EXISTENCE of a resource.
    """
    __tablename__ = 'references'

    uri = Column('uri', String, primary_key=True)
    real_uri = Column('real_uri', String)

    type = Column('type', String)
    provider = Column('provider', String)

    @classmethod
    def add(cls, session, item):
        """ [ Initial Source Reference ]
        Add initial ref with NEW real_uri
        """
        real_uri = '{}:{}:{}'.format(
            item.provider, item.type, str(uuid.uuid1().hex)
        )
        ref = cls.bind(session, item, real_uri)
        return ref

    @classmethod
    def add_resources(cls, session, items):
        all = []
        for item in items:
            all.append( cls.add(session, item) )
        session.commit()
        return all

    @classmethod
    def bind(cls, session, item, real_uri):
        ref = cls(
            uri=item.uri,
            real_uri=real_uri,
            type=item.type,
            provider=item.provider
        )
        session.merge(ref)
        #session.commit()  #-> Better to commit after multiple inserts
        return ref

    @classmethod
    def bind_resources(cls, session, pairs):
        """ [ Add batch references ]
        This method is called when:
          - It's already known which refers to which.
          - The "ref_items" has to be stricly in the format of
            [(item, 'real_uri'), (item, 'real_uri'), ....]
        """
        all = []
        for item, real_uri in pairs:
            ref = cls.bind(session, item, real_uri)
            all.append(ref)
        session.commit()
        print('[  OK  ] Inserted {} references.'.format(
            len(all)
        ))
        return all





# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================


def main():
    #------- Start of Data Submitting ---------

    # Clearout all existing tables
    try:
        Reference.__table__.drop(engine)
        pass
    except Exception as e:
        print('Error on dropping User table.')

    # Let new Schemas take effect
    Base.metadata.create_all(bind=engine)

    #------- End of Data Submitting ---------



if __name__ == '__main__':
    main()



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
