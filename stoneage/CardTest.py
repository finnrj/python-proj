#! /usr/bin/env python3

import unittest
from Card import Card
from Player import Player
from Strategy import StupidBot

class CardTest(unittest.TestCase):
    
    def setUp(self):
        self.activePlayer = Player("Red", StupidBot())
        self.opponentBlue = Player("Blue", StupidBot())
        self.opponentGreen = Player("Green", StupidBot())
        
        self.players = [self.activePlayer, self.opponentBlue, self.opponentGreen]
        
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
        self.artCardg = Card("art", "roll", 6)
        
        self.writingCard = Card("writing", "extracard", 1)
    
    def testCardGetSymbol(self):
        self.assertEqual("pottery", self.potCard.getSymbol())
            
    def testPotCardAction(self):
        self.assertEqual(12 * [2], self.activePlayer.getFood())
        self.activePlayer.addCard(self.potCard, self.players)
        self.assertEqual(19 * [2], self.activePlayer.getFood())

    def testArtCardAction(self):
        self.assertEqual([0,0,0], self.activePlayer.getTools())
        self.activePlayer.addCard(self.artCard, self.players)
        self.assertEqual([1,0,0], self.activePlayer.getTools())

    def testHealCardAction(self):
        self.assertEqual(12 * [2], self.activePlayer.getFood())
        self.activePlayer.addCard(self.healCard5, self.players)
        self.assertEqual(17 * [2], self.activePlayer.getFood())
       
        self.assertEqual([], self.activePlayer.getNonFood())
        self.activePlayer.addCard(self.healCard2, self.players)
        self.assertEqual(2 * [10], self.activePlayer.getNonFood())
        
    def testWeaveCardAction(self):
        self.assertEqual(12 * [2], self.activePlayer.getFood())
        self.activePlayer.addCard(self.weaveCard3, self.players)
        self.assertEqual((12 + 3) * [2], self.activePlayer.getFood())
        self.activePlayer.addCard(self.weaveCard1, self.players)
        self.assertEqual((12 + 4) * [2], self.activePlayer.getFood())
 
    def testTimeCardAction(self):
        self.assertEqual(0, self.activePlayer.getFoodTrack())
        self.activePlayer.addCard(self.timeCardft, self.players)
        self.assertEqual(1, self.activePlayer.getFoodTrack())

    def testTransCardAction(self):
        self.assertEqual([], self.activePlayer.getNonFood())
        self.activePlayer.addCard(self.transCard2, self.players)
        self.assertEqual([5,5], self.activePlayer.getNonFood())
    
    def testMusicCardAction(self):
        self.assertEqual(0, self.activePlayer.getScore())
        self.activePlayer.addCard(self.musicCard, self.players)
        self.assertEqual(3, self.activePlayer.getScore())
        
    def testCardWithChristmas(self):
        for player in self.players:
            self.assertEqual([], player.getNonFood())
            self.assertEqual(0, player.getFoodTrack())
            self.assertEqual([0,0,0], player.getTools())

        self.activePlayer.addCard(self.timeCardc, self.players)
        
        for player in self.players:
            if player.getNonFood():
                self.assertEqual(0, player.getFoodTrack())
                self.assertEqual([0,0,0], player.getTools())
            elif [1,0,0] == player.getTools(): 
                self.assertEqual([], player.getNonFood())
                self.assertEqual(0, player.getFoodTrack())
            else: # got a food-track
                self.assertEqual(1, player.getFoodTrack())
                self.assertEqual([], player.getNonFood())
                self.assertEqual([0,0,0], player.getTools())

    def testArtGoldCard(self):
        self.activePlayer.toolbox.upgrade()
        self.activePlayer.toolbox.upgrade()
        self.activePlayer.toolbox.upgrade()
        self.activePlayer.toolbox.upgrade()
        self.assertEqual([], self.activePlayer.getNonFood())
        self.activePlayer.addCard(self.artCardg, self.players)
        self.assertTrue(len(self.activePlayer.getNonFood()) > 0)
        self.assertTrue(len(self.activePlayer.getNonFood()) < 3)
        self.assertTrue(6 in self.activePlayer.getNonFood())
        
    def testCardPoints(self):
        self.assertEqual(0, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.potCard, self.players)
        self.assertEqual(1, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.weaveCard3, self.players)
        self.assertEqual(4, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.weaveCard1, self.players)
        self.assertEqual(4 + 1, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.timeCardc, self.players)
        self.assertEqual(9 + 1, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.timeCardft, self.players)
        self.assertEqual(9 + 4, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.healCard5, self.players)
        self.assertEqual(16 + 4, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.healCard2, self.players)
        self.assertEqual(16 + 9, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.transCard2, self.players)
        self.assertEqual(25 + 9, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.musicCard, self.players)
        self.assertEqual(36 + 9, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.artCard, self.players)
        self.assertEqual(49 + 9, self.activePlayer.getCardScore())
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CardTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
# alternatively use this for shorter output
##    unittest.main()
