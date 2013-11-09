class Card(object):
    
    def __init__(self, symbol,action,number):
        self.symbol = symbol
        self.actionType = action
        self.number = number

    def action(self, player):
        if self.actionType == "food":
            player.addResources(self.number * [2])
        elif self.actionType == "foodTrack":
            player.addResources([7])
        elif self.actionType == "stone":
            player.addResources([5,5])
        elif self.actionType == "score":
            player.addScore (self.number)
        elif self.actionType == "tool":
            player.addResources([9])
        elif self.actionType == "joker":
            player.addResources(self.number *  [10])
            
    def execute(self, player):
        self.action(player)
        
    def getSymbol(self):
        return self.symbol