#! /usr/bin/env python3

import unittest
from Resource import Resource, HuntingGrounds, Forest, River, Quarry

class ResourceTest(unittest.TestCase):
    
    def testCount(self):
        rs = River()

        rs.addPerson(1, "r")
        self.assertEqual(1, rs.count("r"))
        
        from Board import PlacementError
        with self.assertRaisesRegex(PlacementError, "Player r already added person to the River"):
            rs.addPerson(1, "r")
        self.assertEqual(1, rs.count("r"))
        
    def testCountTwoPlayers(self):
        rs = River()

        rs.addPerson(1, "r")
        self.assertEqual(1, rs.count("r"))
        self.assertEqual(6, rs.freeSlots())
        
        rs.addPerson(3, "b")
        self.assertEqual(3, rs.count("b"))
        self.assertEqual(3, rs.freeSlots())

    def testCountAfterReaping(self):
        rs = Quarry()
        rs.addPerson(1, "r")
        self.assertEqual(1, rs.count("r"))        
        rs.reapResources("r")
        self.assertEqual(0, rs.count("r"))

    def testReapFoodWith3Persons(self):
        rs = HuntingGrounds()

        rs.addPerson(3, "r")
        food = rs.reapResources("r")

        self.assertIn(len(food), range(1,10))
        self.assertIsInstance(food[0], int)
        self.assertEqual(len(food), food.count(2))

    def testReapFoodWith1Person(self):
        rs = HuntingGrounds()

        rs.addPerson(1, "r")
        food = rs.reapResources("r")

        self.assertIn(len(food), range(0,4))

    def testReapWoodWith2Persons(self):
        rs = Forest()

        rs.addPerson(2, "r")
        wood = rs.reapResources("r")

        self.assertIn(len(wood), range(0,5))
        
    def testReapWoodWith5Persons(self):
        rs = Forest()

        rs.addPerson(5, "r")
        wood = rs.reapResources("r")

        self.assertIn(len(wood), range(1,11))
        self.assertIsInstance(wood[0], int)
        self.assertEqual(len(wood), wood.count(3))

    def testPureResource(self):
        rs = Resource()

        rs.addPerson(1, "r")
        with self.assertRaisesRegex(AttributeError, "object has no attribute 'resourceValue'"):
            rs.reapResources("r")

    


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(ResourceTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    # alternatively use this for shorter output
    ##    unittest.main()

if __name__ == '__main__':
    main()
