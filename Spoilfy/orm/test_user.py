#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import unittest
import json

from common import Base, engine, session, Resource, Reference
from user import UserAccount, UserResource
from spotify import SpotifyAccount



# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

def test_UserAccount():
    # Add a User Account
    with open('./users.json', 'r') as f:
        jsondata = json.loads( f.read() )
        # Create accounts
        accounts = UserAccount.add_resources(jsondata['users'])
        # Initial add reference
        Reference.add_resources(accounts)
        # Bind user account to provider accounts
        # spotify_acc = SpotifyAccount.query.filter().first()
        for acc in SpotifyAccount.query.filter().all():
            user_acc = acc
            #
            #-> It's critical here we use app account's URI as real_uri
            #   because we want the User Account to be the real existence.
            session.merge( Reference(acc,user_acc.uri,1) )
        session.commit()



def test_UserResource():
    # Get a user
    user = UserAccount.query.first()

    # 1.Add User tracks
    items = Reference.query.filter(Reference.type=='track').all()
    UserResource.add_resources(user.uri, items)
    # 2.Add User albums
    items = Reference.query.filter(Reference.type=='album').all()
    UserResource.add_resources(user.uri, items)
    # 3.Add User artists
    items = Reference.query.filter(Reference.type=='artist').all()
    UserResource.add_resources(user.uri, items)
    # 4.Add User playlists
    items = Reference.query.filter(Reference.type=='playlist').all()
    UserResource.add_resources(user.uri, items)




if __name__ == '__main__':
    try:
        UserAccount.__table__.drop(engine)
        UserResource.__table__.drop(engine)
    except Exception as e:
        print('Error on dropping User table.')
    finally:
        Base.metadata.create_all(bind=engine)

    # -> TEST
    test_UserAccount()
    test_UserResource()
