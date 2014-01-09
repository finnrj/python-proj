#! /usr/bin/env python3

import unittest
from Board import Board
from Hut import Hut, SimpleHut
from Player import Player
from Strategy import StupidBot

class BoardTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.redPlayer = Player("Red", StupidBot())
        self.bluePlayer = Player("Blue", StupidBot())
        self.players = [self.redPlayer, self.bluePlayer]

    def testBoardInitialization(self):
        self.assertListEqual([7,7,7,7], self.board.numberOfHutsLeft())
        self.assertEqual(36, self.board.numberOfCardsLeft())

    def testAvailableHuts(self):
        ahs = self.board.availableHuts()
        self.assertEqual(4, len(ahs))
        self.assertIsInstance(ahs[0], Hut)
    
    def testPlaceOnHut(self):
        ahs = self.board.availableHuts()
        targetHut = ahs[0]
        self.board.placeOnHutIndex(0, "r")
        ahs = self.board.availableHuts()
        self.assertEqual(3, len(ahs), "should only be 3 huts left")
        self.assertNotIn(targetHut, ahs, "hut should not be available")

    def testPersonCountAfterPlacingOnHut(self):
        self.assertEqual(0, self.board.personCount("r"))
        self.board.placeOnHutIndex(0, "r")
        self.assertEqual(1, self.board.personCount("r"))
        
        self.assertEqual(0, self.board.personCount("b"))
        self.board.placeOnHutIndex(1, "b")
        self.assertEqual(1, self.board.personCount("b"))
        
    def testPlacePersonsWithoutResources(self):
        self.assertEqual(0, self.board.personCount("r"))
        self.board.addHunters(2, "r")
        self.board.addLumberjacks(2, "r")

        self.assertEqual(4, self.board.personCount("r"))

        self.board.addClayDiggers(1, "r")
        
        self.assertEqual(5, self.board.personCount("r"))
       
    def testIllegalPlacement(self):
        self.board.addStoneDiggers(2, "r")
        
        self.assertEqual(2, self.board.personCount("r"))
        from Board import PlacementError
        with self.assertRaises(PlacementError):
            self.board.addStoneDiggers(1, "r")
        
        self.assertEqual(2, self.board.personCount("r"))
        
    def testIsFinished(self):
        self.board = Board([SimpleHut(3,3,4), SimpleHut(3,3,4), SimpleHut(3,3,4), SimpleHut(3,3,4)])
        self.assertFalse(self.board.isFinished())
        self.board = Board([SimpleHut(3,3,4), SimpleHut(3,3,4), SimpleHut(3,3,4)])
        self.assertTrue(self.board.isFinished())
        
    def testReapResources(self):
        hutForRed = SimpleHut(3, 3, 4)
        hutForBlue = SimpleHut(3, 4, 4)
        self.board = Board([hutForRed, hutForBlue, SimpleHut(3,4,5), SimpleHut(4,5,6)])
        self.board.placeOnHut(hutForRed, "r")
        self.board.placeOnHut(hutForBlue, "b")
        
        huts = self.board.reapResources(self.players)
        self.assertEqual(1, len(huts))
        self.assertEqual([hutForRed], huts)
        self.players.reverse()
        
        huts = self.board.reapResources(self.players)
        self.assertEqual([hutForBlue], huts)

    def testReapResourcesWithFarm(self):
        self.board.placeOnFarm("r")
        self.board.addClayDiggers(4, "r")
        huts = self.board.reapResources(self.players)
        self.assertEqual(1, self.redPlayer.getFoodTrack())

def main():
#    suite = unittest.TestLoader().loadTestsFromTestCase(BoardTest)
#    unittest.TextTestRunner(verbosity=2).run(suite)

    # alternatively use this for shorter output
    unittest.main()

if __name__ == '__main__':
    main()
