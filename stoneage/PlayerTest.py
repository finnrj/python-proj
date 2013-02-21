'''
Created on Nov 22, 2012

@author: finn
'''
import unittest
from Player import Player
from Board import Board
from Hut import SimpleHut


class PlayerTest(unittest.TestCase):


    def setUp(self):
        self.player = Player()
        self.board = Board()
        
    def testPlacePersonsWithoutResources(self):
        nPersonsBefore = self.board.personCount()
        self.player.placePersons(self.board)
        self.assertGreater(self.board.personCount(), nPersonsBefore)

    def testPlaceMax5Persons(self):
        nPersonsBefore = self.board.personCount()
        self.player.placePersons(self.board)
        
        nPersonsAfter = self.board.personCount()
        self.player.placePersons(self.board)
        self.assertEqual(self.board.personCount(), nPersonsAfter)
        self.assertLessEqual(self.board.personCount() - nPersonsBefore, 5)

    def testPlaceMax5PersonsWithPersonOnSimpleHut(self):
        self.board = Board([SimpleHut(3, 3, 4), SimpleHut(3, 3, 5), SimpleHut(3, 3, 6), SimpleHut(3, 4, 5)])
        self.player.addResources([3, 3, 4])
        
        nPersonsBefore = self.board.personCount()
        self.player.placePersons(self.board)
        self.assertGreater(self.board.personCount(), nPersonsBefore)
        self.assertEqual(1, self.board.personCount())
        
        self.player.placePersons(self.board)
        self.assertGreater(self.board.personCount(), 1)
        self.assertEqual(5, self.board.personCount())
        
        self.player.placePersons(self.board)
        self.assertEqual(5, self.board.personCount())
        
    def testBuyingOfTwoSimpleHuts(self):
        self.board = Board([SimpleHut(3, 3, 4), SimpleHut(3, 5, 6), SimpleHut(3, 3, 6), SimpleHut(3, 4, 5)])
        self.player.addResources([3, 3, 4, 3, 4, 5])
        
        self.player.placePersons(self.board)
        self.assertEqual(1, self.board.personCount())

        self.player.placePersons(self.board)
        self.assertEqual(2, self.board.personCount())

        self.player.placePersons(self.board)
        self.assertEqual(5, self.board.personCount())

    def testPlacingOfNoSimpleHutPersons(self):
        self.board = Board([SimpleHut(3, 3, 4), SimpleHut(3, 3, 5), SimpleHut(3, 3, 6), SimpleHut(3, 4, 5)])
        self.player.addResources([3, 3])
        
        self.assertEqual(0, self.board.personCount())
        self.player.placePersons(self.board)
        self.assertEqual(5, self.board.personCount())

    def testFeeding(self):
        self.assertEqual(0, self.player.foodMissing())
        self.player.feed()
        self.assertEqual(0, self.player.foodMissing())
        self.player.feed()
        self.assertEqual(3, self.player.foodMissing())

     
        
        
        
        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
