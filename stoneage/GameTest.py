#! /usr/bin/env python3

'''
Created on Nov 22, 2012

@author: finn
'''
import unittest
from Game import Game
from Player import Player
from Hut import SimpleHut
from Strategy import Strategy


class Test(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.redPlayer = Player("Red", Strategy())
        self.bluePlayer = Player("Blue", Strategy())
        self.yellowPlayer = Player("Yellow", Strategy())
        self.greenPlayer = Player("Green", Strategy())
        for p in [self.redPlayer, self.bluePlayer, self.yellowPlayer, self.greenPlayer]:                
            self.game.addPlayer(p)
    
    def testAddingPlayer(self):
        self.game = Game()  
        self.assertEqual(self.game.playerCount(), 0, "no player at start")
          
        self.game.addPlayer(self.redPlayer)
        self.assertEqual(self.game.playerCount(), 1, "one player added")
  
        self.game.addPlayer(self.bluePlayer)
        self.assertEqual(self.game.playerCount(), 2, "two players added")
  
    def testGameFinished(self):
        self.assertFalse(self.game.finished(), "game should not be finished at start")
          
    def testPlayerOrderAtStart(self):
        self.assertEqual(self.game.playerCount(), 4, "all four players added")
        self.assertListEqual([self.redPlayer, self.bluePlayer, self.yellowPlayer, self.greenPlayer], 
                             self.game.getPlayers())
 
    def testPlayerOrderScore(self):
        self.redPlayer.addScore(3)
        self.bluePlayer.addScore(2)
        self.yellowPlayer.addScore(4)
        self.greenPlayer.addScore(2)
        self.assertListEqual([self.yellowPlayer, self.redPlayer, self.bluePlayer, self.greenPlayer], 
                             self.game.getPlayers())
         
    def testPlayerOrderSecondCriteria(self):
        self.bluePlayer.addResources([3])
        self.assertEqual(self.game.playerCount(), 4, "all four players added")
        self.assertListEqual([self.bluePlayer, self.redPlayer, self.yellowPlayer, self.greenPlayer], 
                             self.game.getPlayers())
        
    def testMixedScores(self):
        self.redPlayer.addResources([3,3,3,3,4,5,5])
        self.redPlayer.buyHut(SimpleHut(4,5,5),[4,5,5])
        
        self.yellowPlayer.addResources([3,3,4,4,4,4,6,6,8,9])
        
        self.bluePlayer.addResources([3,3,4,4,4,4,6,6,9])
      
        self.greenPlayer.addResources([3,3,4,4,4,4,6,6,9])
        self.assertListEqual([self.redPlayer, self.yellowPlayer, self.bluePlayer, self.greenPlayer], 
                             self.game.getPlayers())
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()