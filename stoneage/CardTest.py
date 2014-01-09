#! /usr/bin/env python3

import unittest
from Card import SymbolCard, MultiplierCard
from Player import Player
from Strategy import StupidBot
from Hut import SimpleHut

class CardTest(unittest.TestCase):
    
    def setUp(self):
        self.activePlayer = Player("Red", StupidBot())
        self.opponentBlue = Player("Blue", StupidBot())
        self.opponentGreen = Player("Green", StupidBot())
        self.cardPile = [SymbolCard("weaving", "food", 3), SymbolCard("weaving", "food", 1)]
        
        self.players = [self.activePlayer, self.opponentBlue, self.opponentGreen]
        
        self.potCard = SymbolCard("pottery", "food", 7)
        
        self.weaveCard3 = SymbolCard("weaving", "food", 3)
        self.weaveCard1 = SymbolCard("weaving", "food", 1)
        
        self.timeCardc = SymbolCard("time", "christmas", 0)
        self.timeCardft = SymbolCard("time", "foodTrack", 1)
        
        self.healCard5 = SymbolCard("healing", "food", 5)
        self.healCard2 = SymbolCard("healing", "joker", 2)
        
        self.transCard2 = SymbolCard("transport", "stone", 2)
        
        self.musicCard = SymbolCard("music", "score", 3)
        
        self.artCard = SymbolCard("art", "tool", 1)
        self.artCardg = SymbolCard("art", "roll", 6)
        
        self.writingCard = SymbolCard("writing", "extracard", 1)
        
        self.hutBuilderCard = MultiplierCard("hutBuilder", 1, "christmas", 0)
        self.hutBuilderCard2 = MultiplierCard("hutBuilder", 2, "christmas", 0)
        self.hutBuilderCard3 = MultiplierCard("hutBuilder", 3, "score", 3)

        self.farmerCard = MultiplierCard("farmer", 1, "stone", 1)
        self.farmerCard2 = MultiplierCard("farmer", 1, "foodTrack", 1)
        self.farmerCard3 = MultiplierCard("farmer", 2, "food", 3)        

        self.toolMakerCard = MultiplierCard("toolMaker", 1, "oneTimeTool", 3)        
        self.toolMakerCard2 = MultiplierCard("toolMaker", 1, "oneTimeTool", 4)
        self.toolMakerCard3= MultiplierCard("toolMaker", 2, "oneTimeTool", 2)
    
        self.shamanCard = MultiplierCard("shaman", 1, "stone", 1)
        self.shamanCard2 = MultiplierCard("shaman", 1, "gold", 1)
        self.shamanCard3 = MultiplierCard("shaman", 2, "roll", 3)
            
    def testCardGetSymbol(self):
        self.assertEqual("pottery", self.potCard.getSymbol())
            
    def testPotCardAction(self):
        self.assertEqual(12 * [2], self.activePlayer.getFood())
        self.activePlayer.addCard(self.potCard, self.players, self.cardPile)
        self.assertEqual(19 * [2], self.activePlayer.getFood())

    def testArtCardAction(self):
        self.assertEqual([0,0,0], self.activePlayer.getTools())
        self.activePlayer.addCard(self.artCard, self.players, self.cardPile)
        self.assertEqual([1,0,0], self.activePlayer.getTools())

    def testHealCardAction(self):
        self.assertEqual(12 * [2], self.activePlayer.getFood())
        self.activePlayer.addCard(self.healCard5, self.players, self.cardPile)
        self.assertEqual(17 * [2], self.activePlayer.getFood())
       
        self.assertEqual([], self.activePlayer.getNonFood())
        self.activePlayer.addCard(self.healCard2, self.players, self.cardPile)
        self.assertEqual(2 * [10], self.activePlayer.getNonFood())
        
    def testWeaveCardAction(self):
        self.assertEqual(12 * [2], self.activePlayer.getFood())
        self.activePlayer.addCard(self.weaveCard3, self.players, self.cardPile)
        self.assertEqual((12 + 3) * [2], self.activePlayer.getFood())
        self.activePlayer.addCard(self.weaveCard1, self.players, self.cardPile)
        self.assertEqual((12 + 4) * [2], self.activePlayer.getFood())
 
    def testTimeCardAction(self):
        self.assertEqual(0, self.activePlayer.getFoodTrack())
        self.activePlayer.addCard(self.timeCardft, self.players, self.cardPile)
        self.assertEqual(1, self.activePlayer.getFoodTrack())

    def testTransCardAction(self):
        self.assertEqual([], self.activePlayer.getNonFood())
        self.activePlayer.addCard(self.transCard2, self.players, self.cardPile)
        self.assertEqual([5,5], self.activePlayer.getNonFood())
    
    def testMusicCardAction(self):
        self.assertEqual(0, self.activePlayer.getScore())
        self.activePlayer.addCard(self.musicCard, self.players, self.cardPile)
        self.assertEqual(3, self.activePlayer.getScore())
        
    def testCardWithChristmas(self):
        for player in self.players:
            self.assertEqual([], player.getNonFood())
            self.assertEqual(0, player.getFoodTrack())
            self.assertEqual([0,0,0], player.getTools())

        self.activePlayer.addCard(self.timeCardc, self.players, self.cardPile)
        
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
        self.activePlayer.addCard(self.artCardg, self.players, self.cardPile)
        self.assertTrue(len(self.activePlayer.getNonFood()) > 0)
        self.assertTrue(len(self.activePlayer.getNonFood()) < 3)
        self.assertTrue(6 in self.activePlayer.getNonFood())
        
    def testExtraCardCard(self):
        self.assertEqual(0, len(self.activePlayer.cards))
        self.activePlayer.addCard(self.writingCard, self.players, self.cardPile)
        self.assertEqual(2, len(self.activePlayer.cards))
        
    def testHutBuildersCards(self):
        self.activePlayer.huts.append(SimpleHut(3,3,4))
        self.assertEqual(0, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.hutBuilderCard, self.players, self.cardPile)
        self.assertEqual(1, self.activePlayer.getCardScore())
    
        self.activePlayer.addCard(self.hutBuilderCard2, self.players, self.cardPile)
        self.assertEqual(3, self.activePlayer.getCardScore())
        
        self.activePlayer.addCard(self.hutBuilderCard3, self.players, self.cardPile)
        self.assertEqual(6, self.activePlayer.getCardScore())
        
        self.activePlayer.huts.append(SimpleHut(3,3,4))
        self.assertEqual(12, self.activePlayer.getCardScore())

    def testFarmerCards(self):
        self.activePlayer.addResources([8, 8])
        self.assertEqual(0, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.farmerCard, self.players, self.cardPile)
        self.assertEqual(2, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.farmerCard2, self.players, self.cardPile)
        self.assertEqual(6, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.farmerCard3, self.players, self.cardPile)
        self.assertEqual(12, self.activePlayer.getCardScore())

    def testToolMakerCards(self):
        self.activePlayer.addResources([7, 7])
        self.assertEqual(0, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.toolMakerCard, self.players, self.cardPile)
        self.assertEqual(2, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.toolMakerCard2, self.players, self.cardPile)
        self.assertEqual(4, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.toolMakerCard3, self.players, self.cardPile)
        self.assertEqual(8, self.activePlayer.getCardScore())
        
    def testShamanCards(self):
        self.assertEqual(0, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.shamanCard, self.players, self.cardPile)
        self.assertEqual(5, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.shamanCard2, self.players, self.cardPile)
        self.assertEqual(10, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.shamanCard3, self.players, self.cardPile)
        self.assertEqual(20, self.activePlayer.getCardScore())
        
    def testCardPoints(self):
        self.assertEqual(0, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.potCard, self.players, self.cardPile)
        self.assertEqual(1, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.weaveCard3, self.players, self.cardPile)
        self.assertEqual(4, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.weaveCard1, self.players, self.cardPile)
        self.assertEqual(4 + 1, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.timeCardc, self.players, self.cardPile)
        self.assertEqual(9 + 1, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.timeCardft, self.players, self.cardPile)
        self.assertEqual(9 + 4, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.healCard5, self.players, self.cardPile)
        self.assertEqual(16 + 4, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.healCard2, self.players, self.cardPile)
        self.assertEqual(16 + 9, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.transCard2, self.players, self.cardPile)
        self.assertEqual(25 + 9, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.musicCard, self.players, self.cardPile)
        self.assertEqual(36 + 9, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.artCard, self.players, self.cardPile)
        self.assertEqual(49 + 9, self.activePlayer.getCardScore())
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CardTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
# alternatively use this for shorter output
##    unittest.main()
