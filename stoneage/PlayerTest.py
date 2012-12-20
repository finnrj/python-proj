'''
Created on Nov 22, 2012

@author: finn
'''
import unittest
from Player import Player
from Board import Board


class PlayerTest(unittest.TestCase):


    def setUp(self):
        self.player = Player()
        self.board = Board()
        
#    def testSetPersons(self):
#        self.player.setPersons(board) 
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
        minimumResourcesToBuyHut = [3,3,4,4,5,5,6]
        self.player.addResources(minimumResourcesToBuyHut)
        
        nPersonsBefore = self.board.personCount()
        self.player.placePersons(self.board)
#        self.assertGreater(self.board.personCount(), nPersonsBefore)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()