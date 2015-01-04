'''
Created on Nov 22, 2012

@author: finn
'''
import unittest
from Player import Player
from Board import Board
from Hut import SimpleHut, CountHut
from Strategy import StupidBot

class StupidBotStrategyTest(unittest.TestCase):

    def setUp(self):
        self.redPlayer = Player("Red", StupidBot())
        self.bluePlayer = Player("Blue", StupidBot())
        self.board = Board()
        
    def testPlacePersonsWithoutResources(self):
        nPersonsBefore = self.board.personCount(self.redPlayer)
        self.redPlayer.placePersons(self.board)
        self.assertGreater(self.board.personCount(self.redPlayer), nPersonsBefore)

      
    def testPlacingOrderWhenTwoHutsAffordable(self):
        self.board = Board([SimpleHut(3, 3, 4), SimpleHut(3, 5, 6), SimpleHut(3, 3, 6), SimpleHut(3, 4, 5)])
        self.redPlayer.addResources([3, 3, 4, 3, 4, 5])
        
        self.redPlayer.placePersons(self.board)
        self.assertEqual(1, self.board.personCount(self.redPlayer))
        self.assertTrue(self.board.farmOccupied())

        self.redPlayer.placePersons(self.board)
        self.assertEqual(3, self.board.personCount(self.redPlayer))
        self.assertTrue(self.board.breedingHutOccupied())
        
        # occupying the toolsmith with blue player         
        self.assertFalse(self.board.toolSmithOccupied())
        self.board.placeOnToolSmith(self.bluePlayer)
        self.assertEqual(1, self.board.personCount(self.bluePlayer))
        self.assertTrue(self.board.toolSmithOccupied())

        print([str(hut) for hut in self.board.availableHuts()])
        
        self.redPlayer.placePersons(self.board)
        self.assertEqual(4, self.board.personCount(self.redPlayer))
        self.assertEqual(1, self.board.personsOnHuts(self.redPlayer))
        
        print([str(hut) for hut in self.board.availableHuts()])

        self.redPlayer.placePersons(self.board)
        self.assertEqual(5, self.board.personCount(self.redPlayer))
        self.assertEqual(2, self.board.personsOnHuts(self.redPlayer))
        
    def testPlacingOfNoSimpleHutPersons(self):
        self.board = Board([SimpleHut(3, 3, 4), SimpleHut(3, 3, 5), SimpleHut(3, 3, 6), SimpleHut(3, 4, 5)])
        self.redPlayer.addResources([3, 3])
        
        self.redPlayer.placePersons(self.board)
        self.assertEqual(1, self.board.personCount(self.redPlayer))
        self.assertTrue(self.board.farmOccupied())

        self.redPlayer.placePersons(self.board)
        self.assertEqual(3, self.board.personCount(self.redPlayer))
        self.assertTrue(self.board.breedingHutOccupied())
        
        self.redPlayer.placePersons(self.board)
        self.assertEqual(4, self.board.personCount(self.redPlayer))
        self.assertTrue(self.board.toolSmithOccupied())

        self.redPlayer.placePersons(self.board)
        self.assertEqual(5, self.board.personCount(self.redPlayer))

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
        self.redPlayer.addResources([8,8])
        self.assertEqual(1, self.redPlayer.foodMissing())
    
    def testIsPayableBug(self):
        self.redPlayer.addResources([3, 3, 3, 3, 3, 4, 4, 5, 6,])
        firstHut = CountHut(4, 2)

        self.redPlayer.strategy.updatePlannedCosts(firstHut, self.redPlayer.resources)
        
        self.assertDictEqual({firstHut : [3,4,3,3]}, self.redPlayer.strategy.plannedCosts)
        
        secondHut = CountHut(4, 3)
        self.assertTrue(self.redPlayer.isPayable(secondHut))
        self.redPlayer.strategy.updatePlannedCosts(secondHut, self.redPlayer.resources)

        self.assertDictEqual({firstHut : [3,4,3,3], secondHut : [3,4,5,3]}, self.redPlayer.strategy.plannedCosts)
        
        thirdHut = SimpleHut(3, 5, 6)
        self.assertTrue(self.redPlayer.isPayable(thirdHut))
        
        fourthHut = CountHut(5, 2)
        self.assertTrue(self.redPlayer.isPayable(fourthHut))
        
    def testBuyingHutsChangesScore(self):
        self.redPlayer.addResources([3, 3, 4, 3, 4, 5])
        hut1 = SimpleHut(3, 3, 4)
        hut2 = SimpleHut(3, 4, 5)
        self.redPlayer.strategy.plannedCosts = {hut1 : [3,3,4], 
                                             hut2 : [3,4,5]}
        
        self.assertEqual(0, self.redPlayer.score)
        self.redPlayer.buyHuts([hut1, hut2])
        self.assertEqual(22, self.redPlayer.score)
        
    def testFoodTrack(self):
        self.assertEqual(0, self.redPlayer.getFoodTrack())
        self.redPlayer.addResources([8])
        self.assertEqual(1, self.redPlayer.getFoodTrack())
        
        self.redPlayer.addResources([3,3,8])
        self.assertEqual(2, self.redPlayer.getFoodTrack())
        self.assertEqual([3,3], self.redPlayer.getNonFood())
        
        self.redPlayer.addResources([4,8,8,3])
        self.assertEqual(4, self.redPlayer.getFoodTrack())
        self.assertListEqual(sorted([3,3,4,3]), self.redPlayer.getNonFood())
        
    def testFoodTrackMaximum(self):
        self.assertEqual(0, self.redPlayer.getFoodTrack())
        self.redPlayer.addResources(10 * [8])
        self.assertEqual(10, self.redPlayer.getFoodTrack())

        self.redPlayer.addResources([8])
        self.assertEqual(10, self.redPlayer.getFoodTrack())

    def testBreeding(self):
        self.assertEqual(5, self.redPlayer.getPersonCount())
        self.redPlayer.addResources([9])
        self.assertEqual(6, self.redPlayer.getPersonCount())

    def testBreedingMaximum(self):
        self.assertEqual(5, self.redPlayer.getPersonCount())
        self.redPlayer.personCount = 10

        self.redPlayer.addResources([8])
        self.assertEqual(10, self.redPlayer.getPersonCount())

    def testPlaceOnBreedingHut(self):
        self.assertEqual(5, self.redPlayer.personsLeft(self.board))
        self.board.placeOnBreedingHut(self.redPlayer)
        self.assertEqual(3, self.redPlayer.personsLeft(self.board)) 

    def testTools(self):
        self.assertEqual([0, 0, 0], self.redPlayer.getTools())
        self.redPlayer.addResources([7])
        self.assertEqual([1, 0, 0], self.redPlayer.getTools())

    def testToolsToUseWith_100(self):
        self.redPlayer.toolbox.upgrade()
        resourceValue = 3
        eyes = 5
        self.assertEqual(1, self.redPlayer.toolsToUse(resourceValue, eyes))

        resourceValue = 3
        eyes = 4
        self.assertEqual(0, self.redPlayer.toolsToUse(resourceValue, eyes))

    def testToolsToUseWith_110(self):
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        
        resourceValue = 3
        eyes = 4
        self.assertEqual(2, self.redPlayer.toolsToUse(resourceValue, eyes))
        
    def testToolsToUseWith_111(self):
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
                
        resourceValue = 3
        eyes = 4
        self.assertEqual(2, self.redPlayer.toolsToUse(resourceValue, eyes))


    def testToolsToUseWith_221_rv4(self):
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
                
        resourceValue = 4
        eyes = 1
        self.assertEqual(3, self.redPlayer.toolsToUse(resourceValue, eyes))

    def testToolsToUseWith_221(self):
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
                
        resourceValue = 3
        eyes = 5
        self.assertEqual(4, self.redPlayer.toolsToUse(resourceValue, eyes))

    def testToolsToUseWith_222(self):
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        
        resourceValue = 6
        eyes = 3
        self.assertEqual(4, self.redPlayer.toolsToUse(resourceValue, eyes))

    def testToolsToUseWith_444(self):
        for index in range(1,13):
            self.redPlayer.toolbox.upgrade()
        
        resourceValue = 3
        eyes = 4
        self.assertEqual(12, self.redPlayer.toolsToUse(resourceValue, eyes))

    def testToolsToUseWith_322(self):
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
        self.redPlayer.toolbox.upgrade()
                
        resourceValue = 6
        eyes = 3
        self.assertEqual(3, self.redPlayer.toolsToUse(resourceValue, eyes))        
        
    def testReapingOrder(self):
        self.assertEqual("g", self.redPlayer.chooseReapingResource("fsg"))
        self.assertEqual("s", self.redPlayer.chooseReapingResource("fs"))
        self.assertEqual("s", self.redPlayer.chooseReapingResource("fwcs"))
        self.assertEqual("c", self.redPlayer.chooseReapingResource("fwc"))
        
    def testChooseChristmas(self):
        self.assertEqual(0, self.redPlayer.getFoodTrack())
        self.assertListEqual([3,4,7], self.redPlayer.chooseChristmas([3,4,7,8]))
        self.assertEqual(1, self.redPlayer.getFoodTrack())
        
        self.assertEqual([0,0,0], self.redPlayer.getTools())
        self.assertListEqual([3,4], self.redPlayer.chooseChristmas([3,4,7]))
        self.assertEqual([1,0,0], self.redPlayer.getTools())
        
        self.assertEqual([], self.redPlayer.getNonFood())
        self.assertListEqual([3], self.redPlayer.chooseChristmas([3,4]))
        self.assertEqual([4], self.redPlayer.getNonFood())

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(StupidBotStrategyTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
