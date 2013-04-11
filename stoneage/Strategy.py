from Hut import AnyHut
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
    
    def buyHuts(self, huts):
        raise StrategyNotImplemented("The buyHuts() method should be implemented")
    
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
        
    def buyHuts(self, huts):
        plannedResources = [cost for costs in self.player.plannedCosts.values() for cost in costs]
        for resource in plannedResources:
            self.player.resources.remove(resource)
        self.player.huts.extend(huts)
        self.player.score += sum([hut.value() for hut in huts])
        return huts

class Human(Strategy):
    """Class for a human player"""
    
    prompt = """Please place persons!
        Inputformat: [location][number], where

            Grounds:                
                Hunting: f
                Forest : w
                Clay:    c
                Quarry:  s
                River:   g

            Hut (building): h
    """
    
    def placePersons(self, player, board):
        inputString = input(self.prompt)
        self.processPlacePersonsInput(inputString, board)
    
    def processPlacePersonsInput(self, inp, board):
        inp = inp.lower()
        abr = self.player.getAbr()
        
        sa = inp[:1] #String argument
        number = int(inp[1:])
        if   sa == "f":   board.addHunters(number, abr)
        elif sa == "w": board.addLumberjacks(number, abr)
        elif sa == "c": board.addClayDiggers(number, abr)
        elif sa == "s": board.addStoneDiggers(number, abr)
        elif sa == "g": board.addGoldDiggers(number, abr)
        elif sa == "h": board.placeOnHut(board.availableHuts()[number-1], abr)

    def buyHuts(self, huts):
        result = [] 
        print("You have placed on following huts: " + " ".join(hut.toString() for hut in huts))
        for hut in huts:
            inputString = input(" ".join(["do you want to buy this hut:", hut.toString(), "? (Y|n)"]))
            if inputString != "n":
                self.processBuyHutInput(result, hut)
        return result
    
    def processBuyHutInput(self, result, hut):
        self.player.huts.append(hut)
        self.player.score += self.pay(hut)
        result.append(hut)
            
    def pay(self, hut):
        if hut.hutAsString().startswith("[Any") or hut.hutAsString().startswith("[Count"):
            return sum(self.processPayHut(self.fetchResourecestoPay(hut)))
        else:
            self.player.removeResources(hut.costs([]))
            return hut.value()
    
    def fetchResourecestoPay(self, hut):
        finished = False
        while not finished:
            promptString = " ".join(["choose resources e.g.: 445...", str(self.player.getNonFood()), " "])
            inputString = input(promptString)
            inputResources = [int(ch) for ch in inputString]
            clone = self.player.resources[:]
            try:
                for r in inputResources:
                    clone.remove(r)
            except ValueError:
                print(" ".join(["Resources %s not available in " % inputString, str(self.player.getNonFood()), "\n"]))
                continue # continue while loop ;-)

            if isinstance(hut, AnyHut):
                finished = len(inputString) > 0 and len(inputString) < 8
            else: # CountHut
                if len(hut.missing(inputResources)) != 0:
                    print("missing resources: " + str(hut.missing(inputResources)))
                if len(inputResources) != hut.getResourceCount():
                    print("Given resource count:" + str(len(inputResources)) + ", required: " + str(hut.getResourceCount()))
                finished = (len(hut.missing(inputResources)) == 0) and (len(inputResources) == hut.getResourceCount())  
        return inputString

    def processPayHut(self, inputString):
        costs = [int(ch) for ch in inputString]
        self.player.removeResources(costs)
        return costs

        
        
        
    
    
    