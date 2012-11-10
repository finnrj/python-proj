#! /usr/bin/env python3

from Resource import Resource, HuntingGrounds, Forest
import unittest

class ResourceTest(unittest.TestCase):

    def testReapFoodWith3Persons(self):
        rs = HuntingGrounds()

        rs.addPerson(3)
        food = rs.reapResources()

        self.assertIn(food, range(1,10))

    def testReapFoodWith1Person(self):
        rs = HuntingGrounds()

        rs.addPerson(1)
        food = rs.reapResources()

        self.assertIn(food, range(0,4))

    def testReapWoodWith2Persons(self):
        rs = Forest()

        rs.addPerson(2)
        wood = rs.reapResources()

        self.assertIn(wood, range(0,5))
        
    def testReapWoodWith5Persons(self):
        rs = Forest()

        rs.addPerson(5)
        wood = rs.reapResources()

        self.assertIn(wood, range(1,11))

    def testPureResource(self):
        rs = Resource()

        rs.addPerson(1)
        with self.assertRaisesRegex(AttributeError, "object has no attribute 'resourceValue'"):
            rs.reapResources()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ResourceTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
# alternatively use this for shorter output
##    unittest.main()
