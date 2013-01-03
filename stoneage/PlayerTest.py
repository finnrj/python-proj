'''
Created on Nov 22, 2012

@author: finn
'''
import unittest
from Player import Player
from Board import Board
from Hut import Hut


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

    def testPlaceMax5PersonsWithPersonOnHut(self):
        self.board = Board([Hut(3, 3, 4), Hut(3, 3, 5), Hut(3, 3, 6), Hut(3, 4, 5)])
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
        
    def testBuyingOfTwoHuts(self):
        self.board = Board([Hut(3, 3, 4), Hut(3, 3, 5), Hut(3, 3, 6), Hut(3, 4, 5)])
        self.player.addResources([3, 3, 4, 3, 4, 5])
        
        self.player.placePersons(self.board)
        self.assertEqual(1, self.board.personCount())

        self.player.placePersons(self.board)
        self.assertEqual(2, self.board.personCount())

        self.player.placePersons(self.board)
        self.assertEqual(5, self.board.personCount())

    def testPlacingOfNonHutPersons(self):
        self.board = Board([Hut(3, 3, 4), Hut(3, 3, 5), Hut(3, 3, 6), Hut(3, 4, 5)])
        self.player.addResources([3, 3])
        
        self.assertEqual(0, self.board.personCount())
        self.player.placePersons(self.board)
        self.assertEqual(5, self.board.personCount())

    def testPrint(self):
        self.player.addResources([3, 3, 4, 5])
        self.player.addHuts([Hut(3,3,4), Hut(4,5,6)])
        
        self.player.printPlayer()

        
        
        
        
        
        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
