#! /usr/bin/env python3

from Resource import Resource
import unittest

class ResourceTest(unittest.TestCase):

    def testGetFoodWith3Persons(self):
        rs = Resource("food")

        rs.addPerson(3)
        food = rs.getResources()

        self.assertTrue(food in range(1,10))

    def testGetFoodWith1Person(self):
        rs = Resource("food")

        rs.addPerson(1)
        food = rs.getResources()

        self.assertTrue(food in range(0,4))

    def testGetWoodWith2Persons(self):
        rs = Resource("wood")

        rs.addPerson(2)
        wood = rs.getResources()

        self.assertTrue(wood in range(0,5))
        
    def testGetWoodWith5Persons(self):
        rs = Resource("wood")

        rs.addPerson(5)
        wood = rs.getResources()

        self.assertTrue(wood in range(1,11))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ResourceTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
# alternatively use this for shorter output
##    unittest.main()
