#! /usr/bin/env python3

from Resource import Resource, HuntingGrounds, Forest
import unittest

class ResourceTest(unittest.TestCase):

    def testReapFoodWith3Persons(self):
        rs = HuntingGrounds()

        rs.addPerson(3)
        food = rs.reapResources()

        self.assertIn(len(food), range(1,10))
        self.assertIsInstance(food[0], int)
        self.assertEquals(len(food), food.count(2))

    def testReapFoodWith1Person(self):
        rs = HuntingGrounds()

        rs.addPerson(1)
        food = rs.reapResources()

        self.assertIn(len(food), range(0,4))

    def testReapWoodWith2Persons(self):
        rs = Forest()

        rs.addPerson(2)
        wood = rs.reapResources()

        self.assertIn(len(wood), range(0,5))
        
    def testReapWoodWith5Persons(self):
        rs = Forest()

        rs.addPerson(5)
        wood = rs.reapResources()

        self.assertIn(len(wood), range(1,11))
        self.assertIsInstance(wood[0], int)
        self.assertEquals(len(wood), wood.count(3))

    def testPureResource(self):
        rs = Resource()

        rs.addPerson(1)
        with self.assertRaisesRegex(AttributeError, "object has no attribute 'resourceValue'"):
            rs.reapResources()


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(ResourceTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    # alternatively use this for shorter output
    ##    unittest.main()

if __name__ == '__main__':
    main()
