#! /usr/bin/env python3

from Board import Board
from Hut import Hut
import unittest
from Resource import PlacementError

class BoardTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def tearDown(self):
        self.board.reapResources()
        
    def testBoardInitialization(self):
        self.assertListEqual([4,4,4,5], self.board.numberOfHutsLeft())

    def testAvailableHuts(self):
        ahs = self.board.availableHuts()
        self.assertEqual(4, len(ahs))
        self.assertIsInstance(ahs[0], Hut)
    
    def testPlaceOnHut(self):
        ahs = self.board.availableHuts()
        targetHut = ahs[0]
        self.board.placeOnHut(targetHut)
        ahs = self.board.availableHuts()
        self.assertEqual(3, len(ahs), "should only be 3 huts left")
        self.assertNotIn(targetHut, ahs, "hut should not be available")
        
    def testPlacePersonsWithoutResources(self):
        self.board.addHunters(2)
        self.board.addLumberjacks(2)

        self.assertEqual(4, self.board.personCount())

        self.board.addClayDiggers(1)
        
        self.assertEqual(5, self.board.personCount())
       
    def testIllegalPlacement(self):
        self.board.addStoneDiggers(2)
        
        self.assertEqual(2, self.board.personCount())
        with self.assertRaises(PlacementError):
            self.board.addStoneDiggers(1)
        
        self.assertEqual(2, self.board.personCount())
        
    def testNoBuildingTilesLeft(self):
        nBuildingTiles = self.board.numberOfHutsLeft()
        
        

def main():
##    suite = unittest.TestLoader().loadTestsFromTestCase(BoardTest)
##    unittest.TextTestRunner(verbosity=2).run(suite)

    # alternatively use this for shorter output
    unittest.main()

if __name__ == '__main__':
    main()
