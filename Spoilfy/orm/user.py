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
from common import Base, engine, session, Resource, Reference
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

    #-> Drop default identifiers from PARENT class
    uri = name = id = provider = None

    # -> PKs
    real_uri = Column('real_uri', String, primary_key=True)
    owner_uri = Column('owner_uri', String)

    def __init__(self, owner_uri, data):
        super().__init__(
            real_uri=data.real_uri,
            owner_uri=owner_uri,
            type=data.type
        )

    @classmethod
    def add_resources(cls, owner_uri, references):
        all = []
        for ref in references:
            all.append( session.merge( cls(owner_uri, ref) ) )
            session.commit()
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

    @classmethod
    def loads(cls, jsondata):
        # Create accounts
        accounts = cls.add_resources(jsondata['users'])

        # Initial add reference
        Reference.add_resources(accounts)

        # Bind user account to provider accounts
        # spotify_acc = SpotifyAccount.query.filter().first()
        for acc in SpotifyAccount.query.filter().all():
            user_acc = acc
            #
            #-> It's critical here we use app account's URI as real_uri
            #   because we want the User Account to be the real existence.
            session.merge( Reference(acc, user_acc.uri, 1) )
        session.commit()

    def bind_resources(self, references):
        UserResource.add_resources( self.uri, references )



print('[  OK  ] __IMPORTED__: {}'.format(__name__))
