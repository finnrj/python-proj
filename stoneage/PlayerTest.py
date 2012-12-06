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

#    def testSetPersons(self):
#        self.player.setPersons(board) 
    def testPlacePersonsWithoutResources(self):
        board = Board()
        nPersonsBefore = board.personCount()
        self.player.placePersons(board)
        self.assertEqual(board.personCount(), nPersonsBefore, "no person should be placed")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()