class StrategyNotImplemented(Exception):
    """Exception class for not inheriting the Strategy class"""
    def __init__(self, msg):
        Exception.__init__(self, msg)

class Strategy:
    '''
    classdocs
    '''
    
    def placePersons(self, player, board):
        raise StrategyNotImplemented("The placePersons() method should be implemented")
    
class StupidBot(Strategy):
    
    def placePersons(self, player, board):
        if player.isNewRound(board):
            player.plannedCosts = {}
        
       
        # check huts
        payableHut = player.fetchPayableHut(board.availableHuts())
        if payableHut is not None:
            board.placeOnHut(payableHut, player.abr)
            player.adjustResources(payableHut)
            return
        # place on resources
        if player.resources.count(3) < 2 and board.freeForestSlots() > 0:
            board.addLumberjacks(min(player.personsLeft(board), board.freeForestSlots()) , player.abr)
        elif player.resources.count(4) < 2 and board.freeClayPitSlots() > 0:
            board.addClayDiggers(min(player.personsLeft(board), board.freeClayPitSlots()), player.abr)
        elif player.resources.count(5) < 2 and board.freeQuarrySlots() > 0:
            board.addStoneDiggers(min(player.personsLeft(board), board.freeQuarrySlots()), player.abr)
        elif board.freeRiverSlots() > 0:
            board.addGoldDiggers(min(player.personsLeft(board), board.freeRiverSlots()), player.abr)
        else:
            board.addHunters(player.personsLeft(board), player.abr)
        

class Human(Strategy):
    def placePersons(self, player, board):
        inputString = input("Please do something!")
        self.processInput(inputString, board)
    
    def processInput(self, inp, board):
        inp = inp.lower()
        
#        Inputformat:
#            
#        [stringAbreviation][number]

#            Grounds:                
#                Hunting: h
#                Forest : f
#                Clay: c
#                Quarry: q
#                River: r
#
#            Building: b



        abr = self.player.getAbr()
        
        number = int(inp[1:])
        sa = inp[:1] #String argument
        if sa == "h":   board.addHunters(number, abr)
        elif sa == "f": board.addLumberjacks(number, abr)
        elif sa == "c": board.addClayDiggers(number, abr)
        elif sa == "q": board.addStoneDiggers(number, abr)
        elif sa == "r": board.addGoldDiggers(number, abr)
        elif sa == "b": board.placeOnHut(board.availableHuts()[number-1], abr)
       
    
    
    
    