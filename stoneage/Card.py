from random import randint
from Resource import Resource

class Card:
    
    def __init__(self, symbol, action, number):
        self.symbol = symbol
        self.actionType = action
        self.number = number

    def action(self, players, cardPile):
        activePlayer = players[0]
        if self.actionType == "food":
            activePlayer.addResources(self.number * [Resource.food])
        elif self.actionType == "foodTrack":
            activePlayer.addResources([Resource.farmer])
        elif self.actionType == "stone":
            activePlayer.addResources([Resource.stone, Resource.stone])
        elif self.actionType == "score":
            activePlayer.addScore (self.number)
        elif self.actionType == "tool":
            activePlayer.addResources([Resource.tool])
        elif self.actionType == "joker":
            activePlayer.addResources(self.number *  [Resource.joker])
        elif self.actionType == "christmas":
            presents = [Resource(randint(3, 8)) for dice in range(0, len(players))]
            for player in players:
                player.chooseChristmas(presents)
        elif self.actionType == "roll":
            eyes = sum([randint(1, 6) for dice in [1,2]])
            numberOfResources = int((eyes + activePlayer.toolsToUse(self.number, eyes))/self.number)
            activePlayer.addResources(numberOfResources * [self.number])
        elif self.actionType == 'extracard':
            activePlayer.cards.append(cardPile.pop())
            
    def execute(self, players, cardPile):
        self.action(players, cardPile)
        
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
    
    
    