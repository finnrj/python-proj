#! /usr/bin/env python3

import unittest
from Card import SymbolCard, MultiplierCard, CardAction, CardMultiplier, CardSymbol
from Player import Player, PlayerColor
from Strategy import StupidBot
from Hut import SimpleHut
from Resource import Resource

class CardTest(unittest.TestCase):
    
    def setUp(self):
        self.activePlayer = Player(PlayerColor.Red, StupidBot())
        self.opponentBlue = Player(PlayerColor.Blue, StupidBot())
        self.opponentGreen = Player(PlayerColor.Green, StupidBot())
        
        self.cardPile = [SymbolCard(CardSymbol.weaving, CardAction.food, 3), 
                         SymbolCard(CardSymbol.weaving, CardAction.food, 1),
                         MultiplierCard(CardMultiplier.hutcount, 1, CardAction.christmas, 0),
                         MultiplierCard(CardMultiplier.foodtrack, 1, CardAction.stone, 1),
                         MultiplierCard(CardMultiplier.personcount, 1, CardAction.stone, 1)]
        
        self.players = [self.activePlayer, self.opponentBlue, self.opponentGreen]
        
        self.potCard = SymbolCard(CardSymbol.pottery, CardAction.food, 7)
        
        self.weaveCard3 = SymbolCard(CardSymbol.weaving, CardAction.food, 3)
        self.weaveCard1 = SymbolCard(CardSymbol.weaving, CardAction.food, 1)
        
        self.timeCardc = SymbolCard(CardSymbol.time, CardAction.christmas, 0)
        self.timeCardft = SymbolCard(CardSymbol.time, CardAction.foodtrack, 1)
        
        self.healCard5 = SymbolCard(CardSymbol.healing, CardAction.food, 5)
        self.healCard2 = SymbolCard(CardSymbol.healing, CardAction.resource, 2)
        
        self.transCard2 = SymbolCard(CardSymbol.transport, CardAction.stone, 2)
        
        self.musicCard = SymbolCard(CardSymbol.music, CardAction.point, 3)
        
        self.artCard = SymbolCard(CardSymbol.art, CardAction.tool, 1)
        self.artCardg = SymbolCard(CardSymbol.art, CardAction.roll, 6)
        
        self.writingCard = SymbolCard(CardSymbol.writing, CardAction.extracard, 1)
        
        self.hutBuilderCard = MultiplierCard(CardMultiplier.hutcount, 1, CardAction.christmas, 0)
        self.hutBuilderCard2 = MultiplierCard(CardMultiplier.hutcount, 2, CardAction.christmas, 0)
        self.hutBuilderCard3 = MultiplierCard(CardMultiplier.hutcount, 3, CardAction.point, 3)

        self.farmerCard = MultiplierCard(CardMultiplier.foodtrack, 1, CardAction.stone, 1)
        self.farmerCard2 = MultiplierCard(CardMultiplier.foodtrack, 1, CardAction.foodtrack, 1)
        self.farmerCard3 = MultiplierCard(CardMultiplier.foodtrack, 2, CardAction.food, 3)        

        self.toolMakerCard = MultiplierCard(CardMultiplier.toolsum, 1, CardAction.onetimetool, 3)        
        self.toolMakerCard2 = MultiplierCard(CardMultiplier.toolsum, 1, CardAction.onetimetool, 4)
        self.toolMakerCard3= MultiplierCard(CardMultiplier.toolsum, 2, CardAction.onetimetool, 2)
    
        self.shamanCard = MultiplierCard(CardMultiplier.personcount, 1, CardAction.stone, 1)
        self.shamanCard2 = MultiplierCard(CardMultiplier.personcount, 1, CardAction.gold, 1)
        self.shamanCard3 = MultiplierCard(CardMultiplier.personcount, 2, CardAction.roll, 3)
            
    def testCardGetSymbol(self):
        self.assertEqual(CardSymbol.pottery, self.potCard.getSymbol())
            
    def testPotCardAction(self):
        self.assertEqual(12 * [Resource.food], self.activePlayer.getFood())
        self.activePlayer.addCard(self.potCard, self.players, self.cardPile)
        self.assertEqual(19 * [Resource.food], self.activePlayer.getFood())

    def testArtCardAction(self):
        self.assertEqual([0,0,0], self.activePlayer.getTools())
        self.activePlayer.addCard(self.artCard, self.players, self.cardPile)
        self.assertEqual([1,0,0], self.activePlayer.getTools())

    def testHealCardAction(self):
        self.assertEqual(12 * [Resource.food], self.activePlayer.getFood())
        self.activePlayer.addCard(self.healCard5, self.players, self.cardPile)
        self.assertEqual(17 * [Resource.food], self.activePlayer.getFood())
       
        self.assertEqual([], self.activePlayer.getNonFood())
        self.activePlayer.addCard(self.healCard2, self.players, self.cardPile)
        self.assertEqual(2 * [Resource.joker], self.activePlayer.getNonFood())
        
    def testWeaveCardAction(self):
        self.assertEqual(12 * [Resource.food], self.activePlayer.getFood())
        self.activePlayer.addCard(self.weaveCard3, self.players, self.cardPile)
        self.assertEqual((12 + 3) * [Resource.food], self.activePlayer.getFood())
        self.activePlayer.addCard(self.weaveCard1, self.players, self.cardPile)
        self.assertEqual((12 + 4) * [Resource.food], self.activePlayer.getFood())
 
    def testTimeCardAction(self):
        self.assertEqual(0, self.activePlayer.getFoodTrack())
        self.activePlayer.addCard(self.timeCardft, self.players, self.cardPile)
        self.assertEqual(1, self.activePlayer.getFoodTrack())

    def testTransCardAction(self):
        self.assertEqual([], self.activePlayer.getNonFood())
        self.activePlayer.addCard(self.transCard2, self.players, self.cardPile)
        self.assertEqual([Resource.stone, Resource.stone], self.activePlayer.getNonFood())
    
    def testMusicCardAction(self):
        self.assertEqual(0, self.activePlayer.getScore())
        self.activePlayer.addCard(self.musicCard, self.players, self.cardPile)
        self.assertEqual(4, self.activePlayer.getScore())
        
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
        self.assertIn(Resource.gold, self.activePlayer.getNonFood())
        self.assertIsInstance(self.activePlayer.getNonFood()[0], Resource) 
        
    def testExtraCardCard(self):
        self.assertEqual(0, len(self.activePlayer.cards))
        self.assertEqual(5, len(self.cardPile))
        self.assertEqual(0, self.activePlayer.getScore())
        self.assertEqual(0, len(self.activePlayer.getNonFood()))
        self.activePlayer.addCard(self.writingCard, self.players, self.cardPile)
        self.assertEqual(2, len(self.activePlayer.cards))
        self.assertEqual(4, len(self.cardPile))
        # 1 symbolcard + 1 x persons
        self.assertEqual(6, self.activePlayer.getCardScore())
        # no stone added from extracard
        self.assertEqual(0, len(self.activePlayer.getNonFood()))
        
    def testExtraCardCardWithTooFewCardsLeft(self):
        self.assertEqual(0, len(self.activePlayer.cards))
        cardPile = self.cardPile[:4]
        self.assertEqual(4, len(cardPile))
        self.activePlayer.addCard(self.writingCard, self.players, cardPile)
        self.assertEqual(1, len(self.activePlayer.cards))
        self.assertEqual(4, len(cardPile))

    def testHutBuildersCards(self):
        self.activePlayer.huts.append(SimpleHut(Resource.wood, Resource.wood, Resource.clay))
        self.assertEqual(0, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.hutBuilderCard, self.players, self.cardPile)
        self.assertEqual(1, self.activePlayer.getCardScore())
    
        self.activePlayer.addCard(self.hutBuilderCard2, self.players, self.cardPile)
        self.assertEqual(3, self.activePlayer.getCardScore())
        
        self.activePlayer.addCard(self.hutBuilderCard3, self.players, self.cardPile)
        self.assertEqual(6, self.activePlayer.getCardScore())
        
        self.activePlayer.huts.append(SimpleHut(Resource.wood, Resource.wood, Resource.clay))
        self.assertEqual(12, self.activePlayer.getCardScore())

    def testFarmerCards(self):
        self.activePlayer.addResources([Resource.foodtrack, Resource.foodtrack])
        self.assertEqual(0, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.farmerCard, self.players, self.cardPile)
        self.assertEqual(2, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.farmerCard2, self.players, self.cardPile)
        self.assertEqual(6, self.activePlayer.getCardScore())
        self.activePlayer.addCard(self.farmerCard3, self.players, self.cardPile)
        self.assertEqual(12, self.activePlayer.getCardScore())

    def testToolMakerCards(self):
        self.activePlayer.addResources([Resource.tool, Resource.tool])
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
        
        
    def testPlacePerson(self):
        self.assertEqual(0, self.activePlayer.getCardScore())
        
        self.assertFalse(self.shamanCard.isOccupied())
        self.assertIsNone(self.shamanCard.isOccupiedBy())
                          
        self.shamanCard.placePerson(self.activePlayer)
        self.assertTrue(self.shamanCard.isOccupied())
        self.assertEqual(self.activePlayer, self.shamanCard.isOccupiedBy())

    def testPlacePersonTwice(self):
        hut = SimpleHut(Resource.wood,Resource.wood,Resource.clay)
        self.shamanCard.placePerson(self.activePlayer)
        from Board import PlacementError
        with self.assertRaisesRegex(PlacementError, "card is already occupied"):
            self.shamanCard.placePerson(self.opponentBlue)
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CardTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
# alternatively use this for shorter output
##    unittest.main()
