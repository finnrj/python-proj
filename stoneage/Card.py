from enum import Enum
from random import randint

from Resource import Resource


class CardAction(Enum):
    christmas, clay, extracard, farmer, food, gold, joker, oneTimeTool, roll, score, stone, tool  = range(1, 13)

class CardSymbol(Enum):
    weaving, time, healing, art, pottery, transport, music, writing = range(1,9)
     
class CardMultiplier(Enum):
    hutBuilder, farmer, toolMaker, shaman = range(1,5)
    
class Card:
    
    def __init__(self, symbol, action, number):
        self.player = None
        self.symbol = symbol
        self.action = action
        self.number = number

    def executeAction(self, players, cardPile):
        activePlayer = players[0]
        if self.action == CardAction.christmas:
            presents = [Resource(randint(3, 8)) for dice in range(0, len(players))]
            for player in players:
                player.chooseChristmas(presents)
        elif self.action == CardAction.clay:
            activePlayer.addResources([Resource.clay])
        elif self.action == CardAction.extracard:
            activePlayer.cards.append(cardPile.pop())
        elif self.action == CardAction.farmer:
            activePlayer.addResources([Resource.farmer])
        elif self.action == CardAction.food:
            activePlayer.addResources(self.number * [Resource.food])
        elif self.action == CardAction.gold:
            activePlayer.addResources([Resource.gold])
        elif self.action == CardAction.joker:
            activePlayer.addResources(self.number *  [Resource.joker])
        elif self.action == CardAction.oneTimeTool:
            pass
        elif self.action == CardAction.roll:
            eyes = sum([randint(1, 6) for dice in ["first", "second"]])
            numberOfResources = int((eyes + activePlayer.toolsToUse(self.number, eyes))/self.number)
            activePlayer.addResources(numberOfResources * [self.number])
        elif self.action == CardAction.score:
            activePlayer.addScore (self.number)
        elif self.action == CardAction.stone:
            activePlayer.addResources(self.number * [Resource.stone])
        elif self.action == CardAction.tool:
            activePlayer.addResources([Resource.tool])
            
    def execute(self, players, cardPile):
        self.executeAction(players, cardPile)
        
    def getSymbol(self):
        return self.symbol
    
    def placePerson(self, player):
        if self.isOccupied():
            from Board import PlacementError
            raise PlacementError("card is already occupied")
        self.player = player

    def removePerson(self):
        self.player = None

    def isOccupied(self):
        return self.player != None

    def isOccupiedBy(self):
        return self.player


    
class SymbolCard(Card):
    def __init__(self, symbol, action, number):
        Card.__init__(self, symbol, action, number)
        self.color = "48;5;118"

    def outputString(self):
        return "action: %s, number: %d, symbol: %s" % (self.action.name, self.number, self.symbol.name)
        
    def __str__(self):
        return "\033[%sm%s\033[0m" % (self.color, self.outputString())

class MultiplierCard(Card):
    def __init__(self, symbol, multiplier, action, number):
        Card.__init__(self, symbol, action, number)
        self.multiplier = multiplier
        self.color = "48;5;136"
        
    def getMultiplier(self):
        return self.multiplier
    
    def outputString(self):
        return "action: %s, %d x %s" % (self.action.name, self.multiplier, self.symbol.name)
    
    def __str__(self):
        return "\033[%sm%s\033[0m" % (self.color, self.outputString())
    
    