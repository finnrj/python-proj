from enum import Enum
from random import randint

from Resource import Resource


class CardAction(Enum):
    food, foodTrack, clay, stone, gold, score, tool, joker, christmas, roll, extracard, oneTimeTool = range(1, 13)
    
class CardSymbol(Enum):
    weaving, time, healing, art, pottery, transport, music, writing = range(1,9)
     
class CardMultiplier(Enum):
    hutBuilder, farmer, toolMaker, shaman = range(1,5)
    
class Card:
    
    def __init__(self, symbol, action, number):
        self.symbol = symbol
        self.action = action
        self.number = number

    def executeAction(self, players, cardPile):
        activePlayer = players[0]
        if self.action == CardAction.food:
            activePlayer.addResources(self.number * [Resource.food])
        elif self.action == CardAction.foodTrack:
            activePlayer.addResources([Resource.farmer])
        elif self.action == CardAction.stone:
            activePlayer.addResources([Resource.stone, Resource.stone])
        elif self.action == CardAction.score:
            activePlayer.addScore (self.number)
        elif self.action == CardAction.tool:
            activePlayer.addResources([Resource.tool])
        elif self.action == CardAction.joker:
            activePlayer.addResources(self.number *  [Resource.joker])
        elif self.action == CardAction.christmas:
            presents = [Resource(randint(3, 8)) for dice in range(0, len(players))]
            for player in players:
                player.chooseChristmas(presents)
        elif self.action == CardAction.roll:
            eyes = sum([randint(1, 6) for dice in [1,2]])
            numberOfResources = int((eyes + activePlayer.toolsToUse(self.number, eyes))/self.number)
            activePlayer.addResources(numberOfResources * [self.number])
        elif self.action == CardAction.extracard:
            activePlayer.cards.append(cardPile.pop())
            
    def execute(self, players, cardPile):
        self.executeAction(players, cardPile)
        
    def getSymbol(self):
        return self.symbol

    
class SymbolCard(Card):
    def __init__(self, symbol, action, number):
        Card.__init__(self, symbol, action, number)

class MultiplierCard(Card):
    def __init__(self, symbol, multiplier, action, number):
        Card.__init__(self, symbol, action, number)
        self.multiplier = multiplier
        
    def getMultiplier(self):
        return self.multiplier
    
    
    