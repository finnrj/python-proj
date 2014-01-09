from random import randint

class Card:
    
    def __init__(self, symbol, action, number):
        self.symbol = symbol
        self.actionType = action
        self.number = number

    def action(self, players, cardPile):
        activePlayer = players[0]
        if self.actionType == "food":
            activePlayer.addResources(self.number * [2])
        elif self.actionType == "foodTrack":
            activePlayer.addResources([8])
        elif self.actionType == "stone":
            activePlayer.addResources([5,5])
        elif self.actionType == "score":
            activePlayer.addScore (self.number)
        elif self.actionType == "tool":
            activePlayer.addResources([7])
        elif self.actionType == "joker":
            activePlayer.addResources(self.number *  [10])
        elif self.actionType == "christmas":
            presents = [randint(3, 8) for dice in range(0, len(players))]
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
    
    
    