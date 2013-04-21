#! /usr/bin/env python3

'''
Created on Dec 21, 2012

@author: finn
'''

import unittest

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover(".", "*Test.py")
    unittest.TextTestRunner(verbosity=2).run(suite)