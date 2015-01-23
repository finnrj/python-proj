#! /usr/bin/env python3

import unittest
from ResourceField import ResourceField, HuntingGrounds, Forest, River, Quarry, Farm,\
    BreedingHut, ToolSmith
from Resource import Resource 
from Board import PlacementError
from Strategy import StupidBot
from Player import Player, PlayerColor


class ResourceTest(unittest.TestCase):
    
    def setUp(self):
        self.redPlayer = Player(PlayerColor.Red, StupidBot())
        self.bluePlayer = Player(PlayerColor.Blue, StupidBot())
            
    def testCount(self):
        rs = River()

        rs.addPerson(1, self.redPlayer)
        self.assertEqual(1, rs.count(self.redPlayer))
        
        with self.assertRaisesRegex(PlacementError, "Player %s already added person to the River" % self.redPlayer.getColor()):
            rs.addPerson(1, self.redPlayer)
        self.assertEqual(1, rs.count(self.redPlayer))
        
    def testCountTwoPlayers(self):
        rs = River()
 
        rs.addPerson(1, self.redPlayer)
        self.assertEqual(1, rs.count(self.redPlayer))
        self.assertEqual(6, rs.freeSlots())
         
        rs.addPerson(3, self.bluePlayer)
        self.assertEqual(3, rs.count(self.bluePlayer))
        self.assertEqual(3, rs.freeSlots())
 
    def testCountAfterReaping(self):
        rs = Quarry()
        rs.addPerson(1, self.redPlayer)
        self.assertEqual(1, rs.count(self.redPlayer))        
        rs.reapResources(self.redPlayer)
        self.assertEqual(0, rs.count(self.redPlayer))
 
    def testReapFoodWith3Persons(self):
        rs = HuntingGrounds()
 
        rs.addPerson(3, self.redPlayer)
        food = rs.reapResources(self.redPlayer)
 
        self.assertIn(len(food), range(1,10))
        self.assertIsInstance(food[0], Resource)
        self.assertEqual(len(food), food.count(Resource.food))
 
    def testReapFoodWith1Person(self):
        rs = HuntingGrounds()
 
        rs.addPerson(1, self.redPlayer)
        food = rs.reapResources(self.redPlayer)
 
        self.assertIn(len(food), range(0,4))
 
    def testReapWoodWith2Persons(self):
        rs = Forest()
 
        rs.addPerson(2, self.redPlayer)
        wood = rs.reapResources(self.redPlayer)
 
        self.assertIn(len(wood), range(0,5))
         
    def testReapWoodWith5Persons(self):
        rs = Forest()
 
        rs.addPerson(5, self.redPlayer)
        wood = rs.reapResources(self.redPlayer)
 
        self.assertIn(len(wood), range(1,11))
        self.assertIsInstance(wood[0], Resource)
        self.assertEqual(len(wood), wood.count(Resource.wood))
 
    def testReapFoodWith3PersonsAndTools_211(self):
        rs = HuntingGrounds()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
         
        rs.addPerson(3, self.redPlayer)
        food = rs.reapResources(self.redPlayer)
 
        self.assertIn(len(food), range(3,12))
 
    def testPureResource(self):
        rs = ResourceField()
 
        rs.addPerson(1, self.redPlayer)
        with self.assertRaisesRegex(AttributeError, "object has no attribute 'resource'"):
            rs.reapResources(self.redPlayer)
 
    def testPlaceOnFarm(self):
        farm = Farm()
         
        self.assertEqual(1, farm.freeSlots())
        farm.addPerson(self.redPlayer)
        self.assertEqual(0, farm.freeSlots())
 
        with self.assertRaises(PlacementError):
            farm.addPerson(self.bluePlayer)
             
    def testFarmResource(self):
        farm = Farm()        
        farm.addPerson(self.redPlayer)
         
        farmResource = farm.reapResources(self.bluePlayer)
        self.assertEqual([], farmResource)
         
        farmResource = farm.reapResources(self.redPlayer)
        self.assertEqual([Resource.foodtrack], farmResource)
         
    def testBreedingHut(self):
        breedingHut = BreedingHut()
        self.assertEqual(2, breedingHut.freeSlots())
        breedingHut.addPerson(self.redPlayer)
        self.assertEqual(0, breedingHut.freeSlots())
 
        breedingResource = breedingHut.reapResources(self.redPlayer)
        self.assertEqual([Resource.person], breedingResource)
 
    def testToolSmith(self):
        toolSmith = ToolSmith()
        self.assertEqual(1, toolSmith.freeSlots())
        toolSmith.addPerson(self.redPlayer)
        self.assertEqual(0, toolSmith.freeSlots())
 
        with self.assertRaises(PlacementError):
            toolSmith.addPerson(self.bluePlayer)
         
        toolResource = toolSmith.reapResources(self.bluePlayer)
        self.assertEqual([], toolResource)
 
        toolResource = toolSmith.reapResources(self.redPlayer)
        self.assertEqual([Resource.tool], toolResource)

def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(ResourceTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    # alternatively use this for shorter output
    ##    unittest.main()

if __name__ == '__main__':
    main()
