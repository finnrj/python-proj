from enum import Enum
from functools import total_ordering
from random import randint

from Resource import Resource


class CardAction(Enum):
    christmas, clay, extracard, foodtrack, food, gold, resource, onetimetool, roll, point, stone, tool  = range(1, 13)

class CardSymbol(Enum):
    weaving, time, healing, art, pottery, transport, music, writing = range(1,9)
     
class CardMultiplier(Enum):
    hutcount, foodtrack, toolsum, personcount = range(1,5)
    
@total_ordering    
class Card:
    
    def __init__(self, symbol, action, number):
        self.player = None
        self.symbol = symbol
        self.action = action
        self.number = number

    def executeAction(self, players, cardPile):
        activePlayer = players[0]
        if self.action == CardAction.christmas:
            presents = [Resource(randint(3, 8)) for dice in range(len(players))]
            for player in players:
                player.chooseChristmas(presents)
        elif self.action == CardAction.clay:
            activePlayer.addResources([Resource.clay])
        elif self.action == CardAction.extracard:
            if len(cardPile) > 4:
                activePlayer.cards.append(cardPile.pop(4))
        elif self.action == CardAction.foodtrack:
            activePlayer.addResources([Resource.foodtrack])
        elif self.action == CardAction.food:
            activePlayer.addResources(self.number * [Resource.food])
        elif self.action == CardAction.gold:
            activePlayer.addResources([Resource.gold])
        elif self.action == CardAction.resource:
            activePlayer.addResources(self.number *  [Resource.joker])
        elif self.action == CardAction.onetimetool:
            activePlayer.addOneTimeTool(self.number)
        elif self.action == CardAction.roll:
            eyes = sum([randint(1, 6) for dice in ["first", "second"]])
            numberOfResources = int((eyes + activePlayer.toolsToUse(self.number, eyes))/self.number)
            activePlayer.addResources(numberOfResources * [Resource(self.number)])
        elif self.action == CardAction.point:
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
    
    def actionString(self):
        if self.action == CardAction.christmas:
            return "%s" % (self.action.name)
        if self.action in [CardAction.clay, CardAction.stone, CardAction.gold, CardAction.extracard, CardAction.food]:
            return "%d %s" % (self.number, self.action.name)
        if self.action in [CardAction.foodtrack, CardAction.tool]:
            return "+1 %s" % (self.action.name)
        if self.action in [CardAction.resource, CardAction.point]:
            return "%d %ss" % (self.number, self.action.name)
        if self.action == CardAction.onetimetool:
            return "OT-tool: %d" % (self.number)
        if self.action == CardAction.roll:
            return "%s for %s" % (self.action.name, Resource(self.number).name)
        
    def suffix(self):
        return self.isOccupied() and self.player.getOutputAbr() or ""
    
    def __lt__(self, other):
        return  self.symbol.name < other.symbol.name  

    def __eq__(self, other):
        return self is other
    
    def __hash__(self):
        return hash("".join([o.__str__() for o in [self.symbol, self.action, self.number]]))
    
class SymbolCard(Card):
    def __init__(self, symbol, action, number):
        Card.__init__(self, symbol, action, number)
        self.color = "48;5;118"

    def outputStrings(self):
        return ["\033[%sm%-15s\033[0m" % (self.color,s) for s in (padString(self.actionString()), padString("%s" %  self.symbol.name))]
        
    def __str__(self):
        return "\033[%sm%s\033[0m" % (self.color, ", ".join(self.outputStrings()))

class MultiplierCard(Card):
    def __init__(self, symbol, multiplier, action, number):
        Card.__init__(self, symbol, action, number)
        self.multiplier = multiplier
        self.color = "48;5;136"
        
    def getMultiplier(self):
        return self.multiplier
    
    def outputStrings(self):
        return ["\033[%sm%-15s\033[0m" % (self.color,s) for s in (padString(self.actionString()), padString("%d x %s" % (self.multiplier, self.symbol.name)))]
    
    def __str__(self):
        return "\033[%sm%s\033[0m" % (self.color, ", ".join(self.outputStrings()))
    
def padString(target, width = 15):
    return ((width - len(target))//2) * " " + target

    