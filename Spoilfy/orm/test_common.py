#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import unittest

from common import engine, Base, Resource, Reference, Include



# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

def test_Resource():
    pass

def test_Reference():
    pass

def test_Include():
    pass




if __name__ == '__main__':
    try:
        Reference.__table__.drop(engine)
        Include.__table__.drop(engine)
    except Exception as e:
        print('Error on dropping User table.')
    finally:
        Base.metadata.create_all(bind=engine)

    # -> 
    test_Resource()
    test_Reference()
    test_Include()



