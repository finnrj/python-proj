'''
Created on Nov 22, 2012

@author: finn
'''
import unittest
from Player import Player, PlayerColor
from Board import Board
from Hut import SimpleHut, CountHut
from Resource import Resource
from Strategy import StupidBot

class StupidBotStrategyTest(unittest.TestCase):

    def setUp(self):
        self.redPlayer = Player(PlayerColor.Red, StupidBot())
        self.bluePlayer = Player(PlayerColor.Blue, StupidBot())
        self.board = Board()
        
    def testPlacePersonsWithoutResources(self):
        nPersonsBefore = self.board.person(self.redPlayer)
        self.redPlayer.placePersons(self.board)
        self.assertGreater(self.board.person(self.redPlayer), nPersonsBefore)

      
    def testPlacingOrderWhenTwoHutsAffordable(self):
        self.board = Board([SimpleHut(Resource.wood, Resource.wood, Resource.clay), SimpleHut(Resource.wood, Resource.stone, Resource.gold), SimpleHut(Resource.wood, Resource.wood, Resource.gold), SimpleHut(Resource.wood, Resource.clay, Resource.stone)])
        self.redPlayer.addResources([Resource.wood, Resource.wood, Resource.clay, Resource.wood, Resource.clay, Resource.stone])
        
        self.redPlayer.placePersons(self.board)
        self.assertEqual(1, self.board.person(self.redPlayer))
        self.assertTrue(self.board.farmOccupied())

        self.redPlayer.placePersons(self.board)
        self.assertEqual(3, self.board.person(self.redPlayer))
        self.assertTrue(self.board.breedingHutOccupied())
        
        # occupying the toolsmith with blue player         
        self.assertFalse(self.board.toolSmithOccupied())
        self.board.placeOnToolSmith(self.bluePlayer)
        self.assertEqual(1, self.board.person(self.bluePlayer))
        self.assertTrue(self.board.toolSmithOccupied())

        self.redPlayer.placePersons(self.board)
        self.assertEqual(4, self.board.person(self.redPlayer))
        self.assertEqual(1, self.board.personsOnHuts(self.redPlayer))
        
        self.redPlayer.placePersons(self.board)
        self.assertEqual(5, self.board.person(self.redPlayer))
        self.assertEqual(2, self.board.personsOnHuts(self.redPlayer))
        
    def testPlacingOfNoSimpleHutPersons(self):
        self.board = Board([SimpleHut(Resource.wood, Resource.wood, Resource.clay), SimpleHut(Resource.wood, Resource.wood, Resource.stone), SimpleHut(Resource.wood, Resource.wood, Resource.gold), SimpleHut(Resource.wood, Resource.clay, Resource.stone)])
        self.redPlayer.addResources([Resource.wood, Resource.wood])
        
        self.redPlayer.placePersons(self.board)
        self.assertEqual(1, self.board.person(self.redPlayer))
        self.assertTrue(self.board.farmOccupied())

        self.redPlayer.placePersons(self.board)
        self.assertEqual(3, self.board.person(self.redPlayer))
        self.assertTrue(self.board.breedingHutOccupied())
        
        self.redPlayer.placePersons(self.board)
        self.assertEqual(4, self.board.person(self.redPlayer))
        self.assertTrue(self.board.toolSmithOccupied())

        self.redPlayer.placePersons(self.board)
        self.assertEqual(5, self.board.person(self.redPlayer))

    def testFeeding(self):
        self.assertEqual(0, self.redPlayer.foodMissing())
        self.redPlayer.feed()
        self.assertEqual(0, self.redPlayer.foodMissing())
        self.redPlayer.feed()
        self.assertEqual(3, self.redPlayer.foodMissing())
        
    
    def testFeedingWithFoodStack(self):
        self.redPlayer.feed()
        self.redPlayer.feed()
        self.assertEqual(3, self.redPlayer.foodMissing())
        self.redPlayer.addResources([Resource.foodtrack,Resource.foodtrack])
        self.assertEqual(1, self.redPlayer.foodMissing())
    
    def testIsPayableBug(self):
        self.redPlayer.addResources([Resource.wood, Resource.wood, Resource.wood, Resource.wood, Resource.wood, Resource.clay, Resource.clay, Resource.stone, Resource.gold,])
        firstHut = CountHut(4, 2)

        self.redPlayer.strategy.updatePlannedCosts(firstHut, self.redPlayer.resources)
        
        self.assertDictEqual({firstHut : [Resource.wood,Resource.clay,Resource.wood,Resource.wood]}, self.redPlayer.strategy.plannedCosts)
        
        secondHut = CountHut(4, 3)
        self.assertTrue(self.redPlayer.isPayable(secondHut))
        self.redPlayer.strategy.updatePlannedCosts(secondHut, self.redPlayer.resources)

        self.assertDictEqual({firstHut : [Resource.wood,Resource.clay,Resource.wood,Resource.wood], secondHut : [Resource.wood,Resource.clay,Resource.stone,Resource.wood]}, self.redPlayer.strategy.plannedCosts)
        
        thirdHut = SimpleHut(Resource.wood, Resource.stone, Resource.gold)
        self.assertTrue(self.redPlayer.isPayable(thirdHut))
        
        fourthHut = CountHut(5, 2)
        self.assertTrue(self.redPlayer.isPayable(fourthHut))
        
    def testBuyingHutsChangesScore(self):
        self.redPlayer.addResources([Resource.wood, Resource.wood, Resource.clay, Resource.wood, Resource.clay, Resource.stone])
        hut1 = SimpleHut(Resource.wood, Resource.wood, Resource.clay)
        hut2 = SimpleHut(Resource.wood, Resource.clay, Resource.stone)
        self.redPlayer.strategy.plannedCosts = {hut1 : [Resource.wood,Resource.wood,Resource.clay], 
                                             hut2 : [Resource.wood,Resource.clay,Resource.stone]}
        
        self.assertEqual(0, self.redPlayer.point)
        self.redPlayer.buyHuts([hut1, hut2])
        self.assertEqual(22, self.redPlayer.point)
        
    def testFoodTrack(self):
        self.assertEqual(0, self.redPlayer.getFoodTrack())
        self.redPlayer.addResources([Resource.foodtrack])
        self.assertEqual(1, self.redPlayer.getFoodTrack())
        
        self.redPlayer.addResources([Resource.wood,Resource.wood,Resource.foodtrack])
        self.assertEqual(2, self.redPlayer.getFoodTrack())
        self.assertEqual([Resource.wood,Resource.wood], self.redPlayer.getNonFood())
        
        self.redPlayer.addResources([Resource.clay,Resource.foodtrack,Resource.foodtrack,Resource.wood])
        self.assertEqual(4, self.redPlayer.getFoodTrack())
        self.assertListEqual(sorted([Resource.wood,Resource.wood,Resource.clay,Resource.wood]), self.redPlayer.getNonFood())
        
    def testFoodTrackMaximum(self):
        self.assertEqual(0, self.redPlayer.getFoodTrack())
        self.redPlayer.addResources(10 * [Resource.foodtrack])
        self.assertEqual(10, self.redPlayer.getFoodTrack())

        self.redPlayer.addResources([Resource.foodtrack])
        self.assertEqual(10, self.redPlayer.getFoodTrack())

    def testBreeding(self):
        self.assertEqual(5, self.redPlayer.getPersonCount())
        self.redPlayer.addResources([9])
        self.assertEqual(6, self.redPlayer.getPersonCount())

    def testBreedingMaximum(self):
        self.assertEqual(5, self.redPlayer.getPersonCount())
        self.redPlayer.person = 10

        self.redPlayer.addResources([Resource.foodtrack])
        self.assertEqual(10, self.redPlayer.getPersonCount())

    def testPlaceOnBreedingHut(self):
        self.assertEqual(5, self.redPlayer.personsLeft(self.board))
        self.board.placeOnBreedingHut(self.redPlayer)
        self.assertEqual(3, self.redPlayer.personsLeft(self.board)) 

    def testTools(self):
        self.assertEqual([0, 0, 0], self.redPlayer.getTools())
        self.redPlayer.addResources([Resource.tool])
        self.assertEqual([1, 0, 0], self.redPlayer.getTools())

    def testToolsToUseWith_100(self):
        self.redPlayer.toolbox.upgrade()
        resource = Resource.wood
        eyes = 5
        self.assertEqual(1, self.redPlayer.toolsToUse(resource, eyes))

        resource = Resource.wood
        eyes = 4
        self.assertEqual(0, self.redPlayer.toolsToUse(resource, eyes))

    def testToolsToUseWith_110(self):
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        
        resource = Resource.wood
        eyes = 4
        self.assertEqual(2, self.redPlayer.toolsToUse(resource, eyes))
        
    def testToolsToUseWith_111(self):
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
                
        resource = Resource.wood
        eyes = 4
        self.assertEqual(2, self.redPlayer.toolsToUse(resource, eyes))


    def testToolsToUseWith_221_rv4(self):
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
                
        resource = Resource.clay
        eyes = 1
        self.assertEqual(3, self.redPlayer.toolsToUse(resource, eyes))

    def testToolsToUseWith_221(self):
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
                
        resource = Resource.wood
        eyes = 5
        self.assertEqual(4, self.redPlayer.toolsToUse(resource, eyes))

    def testToolsToUseWith_222(self):
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        
        resource = Resource.gold
        eyes = 3
        self.assertEqual(4, self.redPlayer.toolsToUse(resource, eyes))

    def testToolsToUseWith_444(self):
        for index in range(1,13):
            self.redPlayer.toolbox.upgrade()
        
        resource = Resource.wood
        eyes = 4
        self.assertEqual(12, self.redPlayer.toolsToUse(resource, eyes))

    def testToolsToUseWith_322(self):
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
                
        resource = Resource.gold
        eyes = 3
        self.assertEqual(3, self.redPlayer.toolsToUse(resource, eyes))
        
    def testToolsToUseWith_000_OneTimeTool_2(self):
        self.redPlayer.addOneTimeTool(2)
        self.assertTrue(len(self.redPlayer.oneTimeTools) == 1)
        
        resource = Resource.wood
        eyes = 4
        self.assertEqual(2, self.redPlayer.toolsToUse(resource, eyes))
        self.assertTrue(len(self.redPlayer.oneTimeTools) == 0)

    def testToolsToUseWith_000_OneTimeTool_3_notUsed(self):
        self.redPlayer.addOneTimeTool(3)
        self.assertTrue(len(self.redPlayer.oneTimeTools) == 1)
        
        resource = Resource.wood
        eyes = 4
        self.assertEqual(0, self.redPlayer.toolsToUse(resource, eyes))
        self.assertTrue(len(self.redPlayer.oneTimeTools) == 1)

    def testToolsToUseWith_000_OneTimeTool_3_Used(self):
        self.redPlayer.addOneTimeTool(3)
        self.assertTrue(len(self.redPlayer.oneTimeTools) == 1)
        
        resource = Resource.clay
        eyes = 5
        self.assertEqual(3, self.redPlayer.toolsToUse(resource, eyes))
        self.assertTrue(len(self.redPlayer.oneTimeTools) == 0)

    def testReapingOrder(self):
        self.assertEqual("g", self.redPlayer.chooseReapingResource("fsg"))
        self.assertEqual("s", self.redPlayer.chooseReapingResource("fs"))
        self.assertEqual("s", self.redPlayer.chooseReapingResource("fwcs"))
        self.assertEqual("c", self.redPlayer.chooseReapingResource("fwc"))
        
    def testChooseChristmas(self):
        self.assertEqual(0, self.redPlayer.getFoodTrack())
        self.assertListEqual([Resource.wood, Resource.clay, Resource.tool],
                             self.redPlayer.chooseChristmas([Resource.wood, Resource.clay, Resource.tool, Resource.foodtrack]))
        self.assertEqual(1, self.redPlayer.getFoodTrack())
        
        self.assertEqual([0,0,0], self.redPlayer.getTools())
        self.assertListEqual([Resource.wood, Resource.clay],
                             self.redPlayer.chooseChristmas([Resource.wood, Resource.clay, Resource.tool]))
        self.assertEqual([1,0,0], self.redPlayer.getTools())
        
        self.assertEqual([], self.redPlayer.getNonFood())
        self.assertListEqual([Resource.wood], self.redPlayer.chooseChristmas([Resource.wood, Resource.clay]))
        self.assertEqual([Resource.clay], self.redPlayer.getNonFood())

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(StupidBotStrategyTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
