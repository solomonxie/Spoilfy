#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:
#   - ./common.py
#   - ./spotify.py

import uuid

#-------[  Import SQLAlchemy ]---------
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, Sequence

#-------[  Import From Other Modules   ]---------
# Package Import Hint: $ python -m Spoilfy.orm.spotify
from common import Base, engine, Resource, Reference
from spotify import SpotifyAccount



# ==============================================================
# >>>>>>>>>>>>>>>>>>[    User's ORMs     ] >>>>>>>>>>>>>>>>>>>
# ==============================================================
"""
Explain:
    User's resources could be:
        Account / Track / Albums / Artist / Playlist
    Except for ACCOUNT, it can store the user's login info.
"""



class UserResource(Resource):
    """ [ User Resources are bit different ]
        User items only store real IDs to REAL resources, like spotify.
    """
    __tablename__ = 'u_Resources'

    real_uri = Column('real_uri', String, primary_key=True)
    owner_uri = Column('owner_uri', String)

    #-> Drop default PK from parent class
    uri = name = id = provider = None

    def __init__(self, owner_uri, data):
        super().__init__(
            real_uri=data.real_uri,
            owner_uri=owner_uri,
            type=data.type
        )
        self.session.merge( self )
        #self.session.commit()  #-> Better to commit after multiple inserts

    @classmethod
    def add_resources(cls, owner_uri, items):
        all = []
        for item in items:
            all.append( cls(owner_uri, item) )

        cls.session.commit()
        print('[  OK  ] Inserted {} items to [{}].'.format(
            len(all), cls.__tablename__
        ))

        return all


class UserAccount(Resource):
    """ [ Store all users registered in THIS system ]
        Explain: UserAccount only store users in current system,
        the user which can have multiple binded accounts from other sites.
        Special setting:
            User Account's Real_URI == Reference's URI
            means in Reference, User's reference is himself.
    """
    __tablename__ = 'u_Accounts'

    password = Column('password', String)
    email = Column('email', String)
    provider = Column('provider', String, default='app')

    def __init__(self, data):
        super().__init__(
            uri = 'app:user:{}'.format(data.get('id')),
            name = data.get('name'),
            id = data.get('id'),
            type = 'user',
            provider = 'app',
            email = data.get('email'),
            password = data.get('password'),
        )
        self.session.merge( self )
        #self.session.commit()  #-> Better to commit after multiple inserts



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
