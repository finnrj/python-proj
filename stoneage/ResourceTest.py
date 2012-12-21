#! /usr/bin/env python3

from Resource import Resource, HuntingGrounds, Forest, River, Quarry, PlacementError
import unittest


class ResourceTest(unittest.TestCase):
    
    def testCount(self):
        rs = River()

        rs.addPerson(1)
        self.assertEqual(1, rs.count())
        
        with self.assertRaisesRegex(PlacementError, "Already added person to this Resource"):
            rs.addPerson(1)
        self.assertEqual(1, rs.count())
        
    def testCountAfterReaping(self):
        rs = Quarry()
        rs.addPerson(1)
        self.assertEqual(1, rs.count())        
        rs.reapResources()
        self.assertEqual(0, rs.count())

    def testReapFoodWith3Persons(self):
        rs = HuntingGrounds()

        rs.addPerson(3)
        food = rs.reapResources()

        self.assertIn(len(food), range(1,10))
        self.assertIsInstance(food[0], int)
        self.assertEqual(len(food), food.count(2))

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
        self.assertEqual(len(wood), wood.count(3))

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
