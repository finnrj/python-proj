#! /usr/bin/env python3

from Hut import Hut
import unittest

class HutTest(unittest.TestCase):

    def testHutPayable(self):
        hut = Hut(3,3,4)
        resources = [3,3,3,4,4]
                
        self.assertEqual([], hut.missing(resources))


    def testHutNotPayable(self):
        hut = Hut(3,3,4)
        resources = [3,4,4,4]
                
        self.assertEqual([3], hut.missing(resources))


    def testHutNotPayable2(self):
        hut = Hut(3,3,4)
        resources = [2,2,3,5,5]
                
        self.assertEqual([3,4], hut.missing(resources))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(HutTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
# alternatively use this for shorter output
##    unittest.main()
