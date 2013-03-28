'''
Created on Nov 22, 2012

@author: finn
'''
import unittest
from Player import Player
from Board import Board
from Hut import SimpleHut, CountHut


class PlayerTest(unittest.TestCase):

    def setUp(self):
        self.player = Player("Red")
        self.board = Board()
        
    def testPlacePersonsWithoutResources(self):
        nPersonsBefore = self.board.personCount("r")
        self.player.placePersons(self.board)
        self.assertGreater(self.board.personCount("r"), nPersonsBefore)

    def testPlaceMax5Persons(self):
        nPersonsBefore = self.board.personCount("r")
        self.player.placePersons(self.board)
        
        nPersonsAfter = self.board.personCount("r")
        self.player.placePersons(self.board)
        self.assertEqual(self.board.personCount("r"), nPersonsAfter)
        self.assertLessEqual(self.board.personCount("r") - nPersonsBefore, 5)

    def testPlaceMax5PersonsWithPersonOnSimpleHut(self):
        self.board = Board([SimpleHut(3, 3, 4), SimpleHut(3, 3, 5), SimpleHut(3, 3, 6), SimpleHut(3, 4, 5)])
        self.player.addResources([3, 3, 4])
        
        nPersonsBefore = self.board.personCount("r")
        self.player.placePersons(self.board)
        self.assertGreater(self.board.personCount("r"), nPersonsBefore)
        self.assertEqual(1, self.board.personCount("r"))
        
        self.player.placePersons(self.board)
        self.assertGreater(self.board.personCount("r"), 1)
        self.assertEqual(5, self.board.personCount("r"))
        
        self.player.placePersons(self.board)
        self.assertEqual(5, self.board.personCount("r"))
        
    def testBuyingOfTwoSimpleHuts(self):
        self.board = Board([SimpleHut(3, 3, 4), SimpleHut(3, 5, 6), SimpleHut(3, 3, 6), SimpleHut(3, 4, 5)])
        self.player.addResources([3, 3, 4, 3, 4, 5])
        
        self.player.placePersons(self.board)
        self.assertEqual(1, self.board.personCount("r"))

        self.player.placePersons(self.board)
        self.assertEqual(2, self.board.personCount("r"))

        self.player.placePersons(self.board)
        self.assertEqual(5, self.board.personCount("r"))

    def testPlacingOfNoSimpleHutPersons(self):
        self.board = Board([SimpleHut(3, 3, 4), SimpleHut(3, 3, 5), SimpleHut(3, 3, 6), SimpleHut(3, 4, 5)])
        self.player.addResources([3, 3])
        
        self.assertEqual(0, self.board.personCount("r"))
        self.player.placePersons(self.board)
        self.assertEqual(5, self.board.personCount("r"))

    def testFeeding(self):
        self.assertEqual(0, self.player.foodMissing())
        self.player.feed()
        self.assertEqual(0, self.player.foodMissing())
        self.player.feed()
        self.assertEqual(3, self.player.foodMissing())
        
    def testIsPayableBug(self):
        self.player.addResources([4, 4, 5, 6, 3, 3, 3, 3, 3])
        firstHut = CountHut(4, 2)
        self.assertTrue(self.player.isPayable(firstHut))
        self.player.adjustResources(firstHut)
        
        self.assertDictEqual({firstHut : [3,4,4,3]}, self.player.plannedCosts)
        
        secondHut = CountHut(4, 3)
        self.assertTrue(self.player.isPayable(secondHut))
        self.player.adjustResources(secondHut)

        self.assertDictEqual({firstHut : [3,4,4,3], secondHut : [3,5,6,3]}, self.player.plannedCosts)
        
        thirdHut = SimpleHut(5, 5, 6)
        self.assertFalse(self.player.isPayable(thirdHut))
        
        fourthHut = CountHut(5, 2)
        self.assertFalse(self.player.isPayable(fourthHut))
        
        
        
        

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(PlayerTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    # import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
