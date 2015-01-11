#! /usr/bin/env python3

import unittest

from Hut import SimpleHut, AnyHut, CountHut
from Player import Player
from Strategy import StupidBot
from Resource import Resource

class HutTest(unittest.TestCase):
    
    def setUp(self):
        self.redPlayer = Player(PlayerColor.Red, StupidBot())

    def testSimpleHutPayable(self):
        hut = SimpleHut(Resource.wood, Resource.wood,Resource.clay)
        resources = [Resource.wood,Resource.wood,Resource.wood,Resource.clay,Resource.clay]
        self.assertEqual([], hut.missing(resources))
        self.assertEqual(10, hut.value(), "value should be 10")

    def testSimpleHutPayableWithOneJoker(self):
        hut = SimpleHut(Resource.wood,Resource.stone,Resource.gold)
        resources = [Resource.wood,Resource.stone,Resource.joker]
        self.assertEqual([], hut.missing(resources))
        self.assertEqual(14, hut.value(), "value should be 14")

    def testSimpleHutPayableWith2Jokers(self):
        hut = SimpleHut(Resource.wood,Resource.stone,Resource.gold)
        resources = [Resource.wood,Resource.joker,Resource.joker]
        self.assertEqual([], hut.missing(resources))
        self.assertEqual(14, hut.value(), "value should be 14")

        hut = SimpleHut(Resource.wood,Resource.stone,Resource.gold)
        resources = [Resource.joker,Resource.stone,Resource.joker]
        self.assertEqual([], hut.missing(resources))
        self.assertEqual(14, hut.value(), "value should be 14")

    def testSimpleHutNotPayable(self):
        hut = SimpleHut(Resource.wood,Resource.wood,Resource.clay)
        resources = [Resource.wood,Resource.clay,Resource.clay,Resource.clay]
                
        self.assertEqual([Resource.wood], hut.missing(resources))

    def testSimpleHutNotPayable2(self):
        hut = SimpleHut(Resource.wood,Resource.wood,Resource.clay)
        resources = [Resource.food,Resource.food,Resource.wood,Resource.stone,Resource.stone]
                
        self.assertEqual([Resource.wood,Resource.clay], hut.missing(resources))

    def testSimpleHutNotPayableWithJoker(self):
        hut = SimpleHut(Resource.wood,Resource.wood,Resource.clay)
        resources = [Resource.food,Resource.food,Resource.wood,Resource.stone,Resource.stone,Resource.joker]
                
        self.assertEqual([Resource.wood], hut.missing(resources))

    def testPlacePerson(self):
        hut = SimpleHut(Resource.wood,Resource.wood,Resource.clay)
        self.assertFalse(hut.isOccupied())
        self.assertIsNone(hut.isOccupiedBy())
        hut.placePerson(self.redPlayer)
        self.assertTrue(hut.isOccupied())
        self.assertEqual(self.redPlayer, hut.isOccupiedBy())

    def testPlacePersonTwice(self):
        hut = SimpleHut(Resource.wood,Resource.wood,Resource.clay)
        hut.placePerson(self.redPlayer)
        from Board import PlacementError
        with self.assertRaisesRegex(PlacementError, "hut is already occupied"):
            hut.placePerson("g")
        
    def testAnyHutWithNoResources(self):
        hut = AnyHut()
        resources = []
        
        self.assertEqual([Resource.wood], hut.missing(resources))

    def testAnyHutWithJokerResource(self):
        hut = AnyHut()
        resources = [Resource.joker]
        
        self.assertEqual([], hut.missing(resources))
        self.assertEqual([Resource.gold], hut.costs(resources))

    def testAnyHutWithResources(self):
        hut = AnyHut()
        resources = [Resource.food,Resource.food,Resource.wood,Resource.stone,Resource.stone]
        
        self.assertEqual([], hut.missing(resources))
        self.assertEqual([Resource.wood,Resource.stone,Resource.stone], hut.costs(resources))

    def testAnyHutWithMoreThanSevenResources(self):
        hut = AnyHut()
        resources = [Resource.wood,Resource.wood,Resource.wood,Resource.stone,Resource.stone,Resource.stone,Resource.stone,Resource.stone]
        
        self.assertEqual([], hut.missing(resources))
        self.assertEqual(0, hut.value(), "value should be 0 before cost is calculated")

        self.assertEqual([Resource.wood,Resource.wood,Resource.wood,Resource.stone,Resource.stone,Resource.stone,Resource.stone], hut.costs(resources))
        self.assertEqual(29, hut.value(), "value should be 29")

    def testAnyHutWithJokerResources(self):
        hut = AnyHut()
        resources = [Resource.food,Resource.food,Resource.wood,Resource.stone,Resource.stone,Resource.joker,Resource.joker]
        
        self.assertEqual([], hut.missing(resources))
        self.assertEqual([Resource.wood,Resource.stone,Resource.stone,Resource.gold,Resource.gold], hut.costs(resources))

    def testAnyHutWithOnlyFood(self):
        hut = AnyHut()
        resources = [Resource.food,Resource.food]
        
        self.assertEqual([Resource.wood], hut.missing(resources))
        self.assertEqual([], hut.costs(resources))
        
    def testCountHutWithNoResources(self):
        hut = CountHut(4,1)
        resources = []
        
        self.assertEqual([Resource.wood,Resource.wood,Resource.wood,Resource.wood], hut.missing(resources))
        
        hut = CountHut(4,3)
        resources = []
        self.assertListEqual([Resource.wood,Resource.wood,Resource.clay,Resource.stone], sorted(hut.missing(resources)))
        
        hut = CountHut(5,4)
        resources = []
        self.assertListEqual([Resource.wood,Resource.wood,Resource.clay,Resource.stone,Resource.gold], sorted(hut.missing(resources)))

    def test_1_TypeCountHutWith_1_JokerResources(self):
        hut = CountHut(4,1)
        resources = [Resource.joker]
        
        self.assertFalse(hut.tooFewDifferentTypes([0,0,0,0], resources.count(Resource.joker)))
        self.assertTrue(hut.tooFewResources(resources))
        
        self.assertEqual([Resource.wood,Resource.wood,Resource.wood], hut.missing(resources))

    def test_2_TypeCountHutWith_1_JokerResources(self):
        hut = CountHut(4,2)
        resources = [Resource.joker]
        
        self.assertTrue(hut.tooFewDifferentTypes([0,0,0,0], resources.count(Resource.joker)))

        self.assertEqual([Resource.wood,Resource.wood,Resource.wood], hut.missing(resources))

    def test_3_TypesCountHutWithOnlyJokerResources(self):
        hut = CountHut(4,3)
        resources = [Resource.joker]
        
        self.assertTrue(hut.tooFewDifferentTypes([0,0,0,0], resources.count(Resource.joker)))
                
        self.assertListEqual([Resource.wood,Resource.wood,Resource.clay], sorted(hut.missing(resources)))

    def test_4_TypesCountHutWithOnlyJokerResources(self):
        hut = CountHut(5,4)
        resources = [Resource.joker]
        
        self.assertTrue(hut.tooFewDifferentTypes([0,0,0,0], resources.count(Resource.joker)))
        
        self.assertListEqual([Resource.wood,Resource.wood,Resource.clay,Resource.stone], sorted(hut.missing(resources)))

    def testCountHutWithEnoughResources(self):
        hut = CountHut(4,2)
        resources = [Resource.food,Resource.food,Resource.wood,Resource.wood,Resource.stone,Resource.stone,Resource.stone]
        
        self.assertEqual([], hut.missing(resources))
        
        hut = CountHut(5,3)
        resources = [Resource.food,Resource.food,Resource.wood,Resource.wood,Resource.stone,Resource.stone,Resource.stone,Resource.gold]
        
        self.assertEqual([], hut.missing(resources))
        
    def testCountHutWithToFewResources(self):
        hut = CountHut(4,2)
        resources = [Resource.food,Resource.food,Resource.wood,Resource.wood,Resource.stone]
        
        self.assertEqual([Resource.wood], hut.missing(resources))
        
        hut = CountHut(4,4)
        resources = [Resource.food,Resource.food,Resource.wood,Resource.wood,Resource.stone]
        self.assertEqual([Resource.clay,Resource.gold], hut.missing(resources))

        hut = CountHut(5,2)
        resources = [Resource.clay,Resource.clay,Resource.clay,Resource.stone]        
        self.assertEqual([Resource.clay], hut.missing(resources))

    def testCountHutCostsWithOnePossiblePayment(self):
        hut = CountHut(4,2)
        resources = [Resource.food,Resource.food,Resource.wood,Resource.wood,Resource.stone,Resource.stone]
        self.assertEqual(0, hut.value(), "value should be 0 before cost is calculated")

        self.assertEqual([Resource.wood,Resource.wood,Resource.stone,Resource.stone], sorted(hut.costs(resources)))
        self.assertEqual(16, hut.value(), "value should be 16")
        
        hut = CountHut(5,3)
        resources = [Resource.food,Resource.food,Resource.wood,Resource.wood,Resource.stone,Resource.stone,Resource.gold]
        self.assertEqual([Resource.wood,Resource.wood,Resource.stone,Resource.stone,Resource.gold], sorted(hut.costs(resources)))
        self.assertEqual(22, hut.value(), "value should be 22")

    def testCountHutCostsWithMorePossiblePayments(self):
        hut = CountHut(4,2)
        resources = [Resource.wood,Resource.wood,Resource.wood,Resource.wood,Resource.stone]
        self.assertEqual([Resource.wood,Resource.wood,Resource.wood,Resource.stone], sorted(hut.costs(resources)))

    def testCountHutCostsWithMorePossiblePayments2(self):
        hut = CountHut(4,2)
        resources = [Resource.stone,Resource.stone,Resource.stone,Resource.wood,Resource.wood,Resource.wood,Resource.clay]
        self.assertEqual([Resource.wood,Resource.wood,Resource.wood,Resource.clay], sorted(hut.costs(resources)))

    def testCountHutCostsWithMorePossiblePayments3(self):
        hut = CountHut(4,2)
        resources = [Resource.wood,Resource.clay,Resource.stone,Resource.stone,Resource.stone]
        self.assertEqual([Resource.wood,Resource.stone,Resource.stone,Resource.stone], sorted(hut.costs(resources)))
        
    def testCountHutError(self):
        hut = CountHut(5, 1)
        resources =  [Resource.wood, Resource.wood, Resource.wood, Resource.gold, Resource.clay, Resource.clay, Resource.clay]
        self.assertEqual([Resource.wood,Resource.wood], hut.missing(resources))

    def testCountHutError2(self):
        hut = CountHut(5, 2)
        resources =  [Resource.clay, Resource.clay, Resource.stone, Resource.gold, Resource.gold]
        self.assertEqual([Resource.clay, Resource.clay], hut.missing(resources))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(HutTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
# alternatively use this for shorter output
##    unittest.main()
