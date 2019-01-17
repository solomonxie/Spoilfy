#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import unittest

from common import engine, Base, Resource, Reference
from common import Include, UnTagged, Incomplete



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
        # Reference.__table__.drop(engine)
        # Include.__table__.drop(engine)
        # UnTagged.__table__.drop(engine)
        # Incomplete.__table__.drop(engine)
        pass
    except Exception as e:
        print('Error on dropping User table.')
    finally:
        Base.metadata.create_all(bind=engine)

    # ->
    test_Resource()
    test_Reference()
    test_Include()



