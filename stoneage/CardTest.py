#! /usr/bin/env python3

import unittest
from Card import Card
from Player import Player
from Strategy import StupidBot

class CardTest(unittest.TestCase):
    
    def setUp(self):
        self.player = Player("Red", StupidBot())
        
        self.potCard = Card("pottery", "food", 7)
        
        self.weaveCard3 = Card("weaving", "food", 3)
        self.weaveCard1 = Card("weaving", "food", 1)
        
        self.timeCardc = Card("time", "christmas", 0)
        self.timeCardft = Card("time", "foodTrack", 1)
        
        self.healCard5 = Card("healing", "food", 5)
        self.healCard2 = Card("healing", "joker", 2)
        
        self.transCard2 = Card("transport", "stone", 2)
        
        self.musicCard = Card("music", "score", 3)
        
        self.artCard = Card("art", "tool", 1)
    
    def testCardGetSymbol(self):
        self.assertEqual("pottery", self.potCard.getSymbol())
            
    def testPotCardAction(self):
        self.assertEqual(12 * [2], self.player.getFood())
        self.player.addCard(self.potCard)
        self.assertEqual(19 * [2], self.player.getFood())

    def testArtCardAction(self):
        self.assertEqual([0,0,0], self.player.getTools())
        self.player.addCard(self.artCard)
        self.assertEqual([1,0,0], self.player.getTools())

    def testHealCardAction(self):
        self.assertEqual(12 * [2], self.player.getFood())
        self.player.addCard(self.healCard5)
        self.assertEqual(17 * [2], self.player.getFood())
       
        self.assertEqual([], self.player.getNonFood())
        self.player.addCard(self.healCard2)
        self.assertEqual(2 * [10], self.player.getNonFood())
        
    def testWeaveCardAction(self):
        self.assertEqual(12 * [2], self.player.getFood())
        self.player.addCard(self.weaveCard3)
        self.assertEqual((12 + 3) * [2], self.player.getFood())
        self.player.addCard(self.weaveCard1)
        self.assertEqual((12 + 4) * [2], self.player.getFood())
 
    def testTimeCardAction(self):
        self.assertEqual(0, self.player.getFoodTrack())
        self.player.addCard(self.timeCardft)
        self.assertEqual(1, self.player.getFoodTrack())

    def testTransCardAction(self):
        self.assertEqual([], self.player.getNonFood())
        self.player.addCard(self.transCard2)
        self.assertEqual([5,5], self.player.getNonFood())
    
    def testMusicCardAction(self):
        self.assertEqual(0, self.player.getScore())
        self.player.addCard(self.musicCard)
        self.assertEqual(3, self.player.getScore())
    
    def testCardPoints(self):
        self.assertEqual(0, self.player.getCardScore())
        self.player.addCard(self.potCard)
        self.assertEqual(1, self.player.getCardScore())
        self.player.addCard(self.weaveCard3)
        self.assertEqual(4, self.player.getCardScore())
        self.player.addCard(self.weaveCard1)
        self.assertEqual(4 + 1, self.player.getCardScore())
        self.player.addCard(self.timeCardc)
        self.assertEqual(9 + 1, self.player.getCardScore())
        self.player.addCard(self.timeCardft)
        self.assertEqual(9 + 4, self.player.getCardScore())
        self.player.addCard(self.healCard5)
        self.assertEqual(16 + 4, self.player.getCardScore())
        self.player.addCard(self.healCard2)
        self.assertEqual(16 + 9, self.player.getCardScore())
        self.player.addCard(self.transCard2)
        self.assertEqual(25 + 9, self.player.getCardScore())
        self.player.addCard(self.musicCard)
        self.assertEqual(36 + 9, self.player.getCardScore())
        self.player.addCard(self.artCard)
        self.assertEqual(49 + 9, self.player.getCardScore())
        
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CardTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
# alternatively use this for shorter output
##    unittest.main()
