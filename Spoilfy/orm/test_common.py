#!/usr/bin/env python3
#
# MAINTAINER: Solomon Xie <solomonxiewise@gmail.com>
#
# DEPENDENCIES:

import unittest

from common import engine, Resource, Reference



# ==============================================================
# >>>>>>>>>>>>>>>>>>>>>>[    TEST     ] >>>>>>>>>>>>>>>>>>>>>>>>
# ==============================================================

def test_Resource():
    pass

def test_Reference():
    try:
        Reference.__table__.drop(engine)
        Reference.metadata.create_all(bind=engine)
    except Exception as e:
        print('Error on dropping User table.')


if __name__ == '__main__':
    test_Resource()
    test_Reference()



