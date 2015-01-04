#! /usr/bin/env python3

import unittest

from Hut import SimpleHut, AnyHut, CountHut
from Player import Player
from Strategy import StupidBot

class HutTest(unittest.TestCase):
    
    def setUp(self):
        self.redPlayer = Player("Red", StupidBot())

    def testSimpleHutPayable(self):
        hut = SimpleHut(3,3,4)
        resources = [3,3,3,4,4]
        self.assertEqual([], hut.missing(resources))
        self.assertEqual(10, hut.value(), "value should be 10")

    def testSimpleHutPayableWithOneJoker(self):
        hut = SimpleHut(3,5,6)
        resources = [3,5,10]
        self.assertEqual([], hut.missing(resources))
        self.assertEqual(14, hut.value(), "value should be 14")

    def testSimpleHutPayableWith2Jokers(self):
        hut = SimpleHut(3,5,6)
        resources = [3,10,10]
        self.assertEqual([], hut.missing(resources))
        self.assertEqual(14, hut.value(), "value should be 14")

        hut = SimpleHut(3,5,6)
        resources = [10,5,10]
        self.assertEqual([], hut.missing(resources))
        self.assertEqual(14, hut.value(), "value should be 14")

    def testSimpleHutNotPayable(self):
        hut = SimpleHut(3,3,4)
        resources = [3,4,4,4]
                
        self.assertEqual([3], hut.missing(resources))

    def testSimpleHutNotPayable2(self):
        hut = SimpleHut(3,3,4)
        resources = [2,2,3,5,5]
                
        self.assertEqual([3,4], hut.missing(resources))

    def testSimpleHutNotPayableWithJoker(self):
        hut = SimpleHut(3,3,4)
        resources = [2,2,3,5,5,10]
                
        self.assertEqual([3], hut.missing(resources))

    def testPlacePerson(self):
        hut = SimpleHut(3,3,4)
        self.assertFalse(hut.isOccupied())
        self.assertIsNone(hut.isOccupiedBy())
        hut.placePerson(self.redPlayer)
        self.assertTrue(hut.isOccupied())
        self.assertEqual(self.redPlayer, hut.isOccupiedBy())

    def testPlacePersonTwice(self):
        hut = SimpleHut(3,3,4)
        hut.placePerson(self.redPlayer)
        from Board import PlacementError
        with self.assertRaisesRegex(PlacementError, "hut is already occupied"):
            hut.placePerson("g")
        
    def testAnyHutWithNoResources(self):
        hut = AnyHut()
        resources = []
        
        self.assertEqual([3], hut.missing(resources))

    def testAnyHutWithJokerResource(self):
        hut = AnyHut()
        resources = [10]
        
        self.assertEqual([], hut.missing(resources))
        self.assertEqual([6], hut.costs(resources))

    def testAnyHutWithResources(self):
        hut = AnyHut()
        resources = [2,2,3,5,5]
        
        self.assertEqual([], hut.missing(resources))
        self.assertEqual([3,5,5], hut.costs(resources))

    def testAnyHutWithMoreThanSevenResources(self):
        hut = AnyHut()
        resources = [3,3,3,5,5,5,5,5]
        
        self.assertEqual([], hut.missing(resources))
        self.assertEqual(0, hut.value(), "value should be 0 before cost is calculated")

        self.assertEqual([3,3,3,5,5,5,5], hut.costs(resources))
        self.assertEqual(29, hut.value(), "value should be 29")

    def testAnyHutWithJokerResources(self):
        hut = AnyHut()
        resources = [2,2,3,5,5,10,10]
        
        self.assertEqual([], hut.missing(resources))
        self.assertEqual([3,5,5,6,6], hut.costs(resources))

    def testAnyHutWithOnlyFood(self):
        hut = AnyHut()
        resources = [2,2]
        
        self.assertEqual([3], hut.missing(resources))
        self.assertEqual([], hut.costs(resources))
        
    def testCountHutWithNoResources(self):
        hut = CountHut(4,1)
        resources = []
        
        self.assertEqual([3,3,3,3], hut.missing(resources))
        
        hut = CountHut(4,3)
        resources = []
        self.assertListEqual([3,3,4,5], sorted(hut.missing(resources)))
        
        hut = CountHut(5,4)
        resources = []
        self.assertListEqual([3,3,4,5,6], sorted(hut.missing(resources)))

    def test_1_TypeCountHutWith_1_JokerResources(self):
        hut = CountHut(4,1)
        resources = [10]
        
        self.assertFalse(hut.tooFewDifferentTypes([0,0,0,0], resources.count(10)))
        self.assertTrue(hut.tooFewResources(resources))
        
        self.assertEqual([3,3,3], hut.missing(resources))

    def test_2_TypeCountHutWith_1_JokerResources(self):
        hut = CountHut(4,2)
        resources = [10]
        
        self.assertTrue(hut.tooFewDifferentTypes([0,0,0,0], resources.count(10)))

        self.assertEqual([3,3,3], hut.missing(resources))

    def test_3_TypesCountHutWithOnlyJokerResources(self):
        hut = CountHut(4,3)
        resources = [10]
        
        self.assertTrue(hut.tooFewDifferentTypes([0,0,0,0], resources.count(10)))
                
        self.assertListEqual([3,3,4], sorted(hut.missing(resources)))

    def test_4_TypesCountHutWithOnlyJokerResources(self):
        hut = CountHut(5,4)
        resources = [10]
        
        self.assertTrue(hut.tooFewDifferentTypes([0,0,0,0], resources.count(10)))
        
        self.assertListEqual([3,3,4,5], sorted(hut.missing(resources)))

    def testCountHutWithEnoughResources(self):
        hut = CountHut(4,2)
        resources = [2,2,3,3,5,5,5]
        
        self.assertEqual([], hut.missing(resources))
        
        hut = CountHut(5,3)
        resources = [2,2,3,3,5,5,5,6]
        
        self.assertEqual([], hut.missing(resources))
        
    def testCountHutWithToFewResources(self):
        hut = CountHut(4,2)
        resources = [2,2,3,3,5]
        
        self.assertEqual([3], hut.missing(resources))
        
        hut = CountHut(4,4)
        resources = [2,2,3,3,5]
        self.assertEqual([4,6], hut.missing(resources))

        hut = CountHut(5,2)
        resources = [4,4,4,5]        
        self.assertEqual([4], hut.missing(resources))

    def testCountHutCostsWithOnePossiblePayment(self):
        hut = CountHut(4,2)
        resources = [2,2,3,3,5,5]
        self.assertEqual(0, hut.value(), "value should be 0 before cost is calculated")

        self.assertEqual([3,3,5,5], sorted(hut.costs(resources)))
        self.assertEqual(16, hut.value(), "value should be 16")
        
        hut = CountHut(5,3)
        resources = [2,2,3,3,5,5,6]
        self.assertEqual([3,3,5,5,6], sorted(hut.costs(resources)))
        self.assertEqual(22, hut.value(), "value should be 22")

    def testCountHutCostsWithMorePossiblePayments(self):
        hut = CountHut(4,2)
        resources = [3,3,3,3,5]
        self.assertEqual([3,3,3,5], sorted(hut.costs(resources)))

    def testCountHutCostsWithMorePossiblePayments2(self):
        hut = CountHut(4,2)
        resources = [5,5,5,3,3,3,4]
        self.assertEqual([3,3,3,4], sorted(hut.costs(resources)))

    def testCountHutCostsWithMorePossiblePayments3(self):
        hut = CountHut(4,2)
        resources = [3,4,5,5,5]
        self.assertEqual([3,5,5,5], sorted(hut.costs(resources)))
        
    def testCountHutError(self):
        hut = CountHut(5, 1)
        resources =  [3, 3, 3, 6, 4, 4, 4]
        self.assertEqual([3,3], hut.missing(resources))

    def testCountHutError2(self):
        hut = CountHut(5, 2)
        resources =  [4, 4, 5, 6, 6]
        self.assertEqual([4, 4], hut.missing(resources))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(HutTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
# alternatively use this for shorter output
##    unittest.main()
