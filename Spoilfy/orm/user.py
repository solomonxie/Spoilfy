#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:
#   - ./common.py
#   - ./spotify.py

import os
import json
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

    #-> Drop default PK from parent class
    uri = name = id = provider = None

    @classmethod
    def add(cls, data):
        item = cls(
            real_uri=data.real_uri,
            type=data.type
        )
        cls.session.merge(item)
        #cls.session.commit()  #-> Better to commit after multiple inserts
        return item


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

    @classmethod
    def add(cls, data):
        user = cls(
            uri = 'app:user:{}'.format(data['id']),
            name = data['name'],
            id = data['id'],
            type = 'user',
            email = data['email'],
            password = data['password']
        )
        cls.session.merge(user)
        #cls.session.commit()  #-> Better to commit after multiple inserts
        return user




# ==============================================================
# >>>>>>>>>>>>>>>>>>>[    METHODS     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================



# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

def test_UserAccount():
    try:
        UserAccount.__table__.drop(engine)
        UserAccount.metadata.create_all(bind=engine)
    except Exception as e:
        print('Error on dropping User table.')

    # Add a User Account
    with open('./users.json', 'r') as f:
        jsondata = json.loads( f.read() )
        # Create accounts
        accounts = UserAccount.add_resources(jsondata['users'])
        # Initial add reference
        Reference.add_resources(accounts)
        # Bind user account to provider accounts
        spotify_acc = SpotifyAccount.query.filter().first()
        user_acc = accounts[0]
        #
        #-> It's critical here we use app account's URI as real_uri
        #   because we want the User Account to be the real existence.
        Reference.bind(spotify_acc, user_acc.uri)



def test_UserResource():
    try:
        UserResource.__table__.drop(engine)
        UserResource.metadata.create_all(bind=engine)
    except Exception as e:
        print('Error on dropping User table.')

    # Add User tracks
    items = Reference.query.filter(Reference.type=='track').all()
    UserResource.add_resources(items)
    ## Add User albums
    #items = session.query(Reference).filter(Reference.type=='album').all()
    #UserResource.add_resources(session, items)
    ## Add User artists
    #items = session.query(Reference).filter(Reference.type=='artist').all()
    #UserResource.add_resources(session, items)
    ## Add User playlists
    #items = session.query(Reference).filter(Reference.type=='playlist').all()
    #UserResource.add_resources(session, items)




if __name__ == '__main__':
    # test_query()
    # test_UserAccount()
    test_UserResource()
