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
        self.player = Player("Red", StupidBot())
        self.board = Board()
        
    def testPlacePersonsWithoutResources(self):
        nPersonsBefore = self.board.personCount("r")
        self.player.placePersons(self.board)
        self.assertGreater(self.board.personCount("r"), nPersonsBefore)

      
    def testPlacingOrderWhenTwoHutsAffordable(self):
        self.board = Board([SimpleHut(3, 3, 4), SimpleHut(3, 5, 6), SimpleHut(3, 3, 6), SimpleHut(3, 4, 5)])
        self.player.addResources([3, 3, 4, 3, 4, 5])
        
        self.player.placePersons(self.board)
        self.assertEqual(1, self.board.personCount("r"))
        self.assertTrue(self.board.farmOccupied())

        self.player.placePersons(self.board)
        self.assertEqual(3, self.board.personCount("r"))
        self.assertTrue(self.board.breedingHutOccupied())

        self.player.placePersons(self.board)
        self.assertEqual(4, self.board.personCount("r"))
        self.assertEqual(1, self.board.personsOnHuts("r"))

        self.player.placePersons(self.board)
        self.assertEqual(5, self.board.personCount("r"))
        self.assertEqual(2, self.board.personsOnHuts("r"))
        
    def testPlacingOfNoSimpleHutPersons(self):
        self.board = Board([SimpleHut(3, 3, 4), SimpleHut(3, 3, 5), SimpleHut(3, 3, 6), SimpleHut(3, 4, 5)])
        self.player.addResources([3, 3])
        
        self.player.placePersons(self.board)
        self.assertEqual(1, self.board.personCount("r"))
        self.assertTrue(self.board.farmOccupied())

        self.player.placePersons(self.board)
        self.assertEqual(3, self.board.personCount("r"))
        self.assertTrue(self.board.breedingHutOccupied())
        
        self.player.placePersons(self.board)
        self.assertEqual(5, self.board.personCount("r"))

    def testFeeding(self):
        self.assertEqual(0, self.player.foodMissing())
        self.player.feed()
        self.assertEqual(0, self.player.foodMissing())
        self.player.feed()
        self.assertEqual(3, self.player.foodMissing())
        
    
    def testFeedingWithFoodStack(self):
        self.player.feed()
        self.player.feed()
        self.assertEqual(3, self.player.foodMissing())
        self.player.addResources([7,7])
        self.assertEqual(1, self.player.foodMissing())
    
    def testIsPayableBug(self):
        self.player.addResources([3, 3, 3, 3, 3, 4, 4, 5, 6,])
        firstHut = CountHut(4, 2)

        self.player.strategy.adjustResources(firstHut, self.player.resources)
        
        self.assertDictEqual({firstHut : [3,4,3,3]}, self.player.strategy.plannedCosts)
        
        secondHut = CountHut(4, 3)
        self.assertTrue(self.player.isPayable(secondHut))
        self.player.strategy.adjustResources(secondHut, self.player.resources)

        self.assertDictEqual({firstHut : [3,4,3,3], secondHut : [3,4,5,3]}, self.player.strategy.plannedCosts)
        
        thirdHut = SimpleHut(5, 5, 6)
        self.assertFalse(self.player.isPayable(thirdHut))
        
        fourthHut = CountHut(5, 2)
        self.assertFalse(self.player.isPayable(fourthHut))
        
    def testBuyingHutsChangesScore(self):
        self.player.addResources([3, 3, 4, 3, 4, 5])
        hut1 = SimpleHut(3, 3, 4)
        hut2 = SimpleHut(3, 4, 5)
        self.player.strategy.plannedCosts = {hut1 : [3,3,4], 
                                             hut2 : [3,4,5]}
        
        self.assertEqual(0, self.player.score)
        self.player.buyHuts([hut1, hut2])
        self.assertEqual(22, self.player.score)
        
    def testFoodTrack(self):
        self.assertEqual(0, self.player.getFoodTrack())
        self.player.addResources([7])
        self.assertEqual(1, self.player.getFoodTrack())
        
        self.player.addResources([3,3,7])
        self.assertEqual(2, self.player.getFoodTrack())
        self.assertEqual([3,3], self.player.getNonFood())
        
        self.player.addResources([4,7,7,3])
        self.assertEqual(4, self.player.getFoodTrack())
        self.assertListEqual(sorted([3,3,4,3]), self.player.getNonFood())
        
    def testFoodTrackMaximum(self):
        self.assertEqual(0, self.player.getFoodTrack())
        self.player.addResources(10 * [7])
        self.assertEqual(10, self.player.getFoodTrack())

        self.player.addResources([7])
        self.assertEqual(10, self.player.getFoodTrack())

    def testBreeding(self):
        self.assertEqual(5, self.player.getPersonCount())
        self.player.addResources([8])
        self.assertEqual(6, self.player.getPersonCount())

    def testBreedingMaximum(self):
        self.assertEqual(5, self.player.getPersonCount())
        self.player.personCount = 10

        self.player.addResources([8])
        self.assertEqual(10, self.player.getPersonCount())

    def testPlaceOnBreedingHut(self):
        self.assertEqual(5, self.player.personsLeft(self.board))
        self.board.placeOnBreedingHut(self.player.getAbr())
        self.assertEqual(3, self.player.personsLeft(self.board)) 

    def testTools(self):
        self.assertEqual([0, 0, 0], self.player.getTools())
        self.player.addResources([9])
        self.assertEqual([1, 0, 0], self.player.getTools())


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(StupidBotStrategyTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
