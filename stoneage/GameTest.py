#! /usr/bin/env python3

from Game import Game
import unittest

class GameTest(unittest.TestCase):

    def testGameInitialization(self):
        game = Game()

        self.assertFalse(game.isFinished(), "game should not be finished")
        self.assertListEqual([7,7,7,7], [len(stack) for stack in game.getBuildingTiles()])

def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(GameTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

    # alternatively use this for shorter output
    ##    unittest.main()

if __name__ == '__main__':
    main()
