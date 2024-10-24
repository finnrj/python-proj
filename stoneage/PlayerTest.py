#! /usr/bin/env python3

import unittest

from Player import Player, PlayerColor
from Card import SymbolCard, CardSymbol
from Strategy import StupidBot
from Resource import Resource

class PlayerTest(unittest.TestCase):
    
    def setUp(self):
        self.redPlayer = Player(PlayerColor.Red, StupidBot())
        self.bluePlayer = Player(PlayerColor.Blue, StupidBot())

    def testgetColor(self):
        self.assertEquals(PlayerColor.Red, self.redPlayer.getColor())
        self.assertEquals(PlayerColor.Blue, self.bluePlayer.getColor())

    def testOutputColor(self):
        self.assertEquals("\x1b[48;5;9mRed\x1b[0m", self.redPlayer.getOutputColor())
        self.assertEquals("\x1b[48;5;33mBlue\x1b[0m", self.bluePlayer.getOutputColor())

    def testgetAbr(self):
        self.assertEquals("r", self.redPlayer.getAbr())
        self.assertEquals("b", self.bluePlayer.getAbr())

    def testgetOutputAbr(self):
        self.assertEquals("\x1b[48;5;9mr\x1b[0m", self.redPlayer.getOutputAbr())
        self.assertEquals("\x1b[48;5;33mb\x1b[0m", self.bluePlayer.getOutputAbr())

    def testScore(self):
        self.assertEquals(0, self.redPlayer.getScore())
        self.bluePlayer.addResources([Resource.food, Resource.wood, Resource.wood])
        self.assertEquals(2, self.bluePlayer.getScore())
        self.bluePlayer.addCard(SymbolCard(CardSymbol.pottery, "food", 7), [self.bluePlayer, self.redPlayer], None)
        self.assertEquals(3, self.bluePlayer.getScore())
                
    def testSecondPointCriteria(self):
        self.assertEquals(5, self.redPlayer.secondScoreCriteria())
        
        self.redPlayer.addResources([Resource.tool,Resource.tool])
        self.assertEquals(7, self.redPlayer.secondScoreCriteria())
        self.redPlayer.addResources([Resource.tool,Resource.tool])
        self.assertEquals(9, self.redPlayer.secondScoreCriteria())
        
        self.redPlayer.addResources([Resource.foodtrack,Resource.foodtrack])
        self.assertEquals(11, self.redPlayer.secondScoreCriteria())
        self.redPlayer.addResources([Resource.foodtrack,Resource.foodtrack])
        self.assertEquals(13, self.redPlayer.secondScoreCriteria())
        
        self.redPlayer.addResources([Resource.person])
        self.assertEquals(14, self.redPlayer.secondScoreCriteria())
        self.redPlayer.addResources([Resource.person])
        self.assertEquals(15, self.redPlayer.secondScoreCriteria())
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(PlayerTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
# alternatively use this for shorter output
##    unittest.main()
