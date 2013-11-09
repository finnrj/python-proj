from random import randint

class Card(object):
    
    def __init__(self, symbol,action,number):
        self.symbol = symbol
        self.actionType = action
        self.number = number

    def action(self, players):
        if self.actionType == "food":
            players[0].addResources(self.number * [2])
        elif self.actionType == "foodTrack":
            players[0].addResources([8])
        elif self.actionType == "stone":
            players[0].addResources([5,5])
        elif self.actionType == "score":
            players[0].addScore (self.number)
        elif self.actionType == "tool":
            players[0].addResources([7])
        elif self.actionType == "joker":
            players[0].addResources(self.number *  [10])
        elif self.actionType == "christmas":
            presents = [randint(3, 8) for dice in range(0, len(players))]
            for player in players:
                player.chooseChristmas(presents)
            
    def execute(self, player):
        self.action(player)
        
    def getSymbol(self):
        return self.symbol