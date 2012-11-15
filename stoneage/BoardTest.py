#! /usr/bin/env python3

from Board import Board
from BuildingTile import BuildingTile
import unittest

class BoardTest(unittest.TestCase):

    def testBoardInitialization(self):
        board = Board()
        self.assertListEqual([4,4,4,5], board.numberOfBuildingTilesLeft())

    def testAvailableBuildingTiles(self):
        board = Board()
        abt = board.availableBuildingTiles()
        self.assertEqual(4, len(abt))
        self.assertIsInstance(abt[0], BuildingTile)

def main():
##    suite = unittest.TestLoader().loadTestsFromTestCase(BoardTest)
##    unittest.TextTestRunner(verbosity=2).run(suite)

    # alternatively use this for shorter output
    unittest.main()

if __name__ == '__main__':
    main()
