from Hut import AnyHut, CountHut

def suffix(object):
    size = object if isinstance(object, type(1)) else len(object)
    return "s" if size > 1 else ""

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
    
    def buyHuts(self, player, huts):
        raise StrategyNotImplemented("The buyHuts() method should be implemented")
    
class StupidBot(Strategy):
    
    def placePersons(self, player, board):
        if player.isNewRound(board):
            player.plannedCosts = {}
        
       
        # check huts
        payableHut = player.fetchPayableHut(board.availableHuts())
        if payableHut is not None:
            board.placeOnHut(payableHut, player.playerAbr)
            player.adjustResources(payableHut)
            return
        # place on resources
        if player.resources.count(3) < 2 and board.freeForestSlots() > 0:
            board.addLumberjacks(min(player.personsLeft(board), board.freeForestSlots()) , player.playerAbr)
        elif player.resources.count(4) < 2 and board.freeClayPitSlots() > 0:
            board.addClayDiggers(min(player.personsLeft(board), board.freeClayPitSlots()), player.playerAbr)
        elif player.resources.count(5) < 2 and board.freeQuarrySlots() > 0:
            board.addStoneDiggers(min(player.personsLeft(board), board.freeQuarrySlots()), player.playerAbr)
        elif board.freeRiverSlots() > 0:
            board.addGoldDiggers(min(player.personsLeft(board), board.freeRiverSlots()), player.playerAbr)
        else:
            board.addHunters(player.personsLeft(board), player.playerAbr)
        
    def buyHuts(self, player,huts):
        plannedResources = [cost for costs in player.plannedCosts.values() for cost in costs]
        for resource in plannedResources:
            player.resources.remove(resource)
        player.huts.extend(huts)
        player.score += sum([hut.value() for hut in huts])
        return huts

class Human(Strategy):
    """Class for a human player"""
    
    prompt = """You have following resource%s: %s 
and %d person%s available. Please place person%s!
     
        Input format: [resource][number], where

            Grounds:                
                Hunting: f
                Forest : w
                Clay:    c
                Quarry:  s
                River:   g
            and 'number' the number of persons to
            place in the chosen ground. 

            Hut: h
            and 'number' is the index of the hut (1-4)
            
    """
   
    def placePersons(self, player, board):
        self.processPlacePersonsInput(self.fetchPlacePersonsInput(player.resources, player.personsLeft(board)), player.getAbr(), board)

    def fetchPlacePersonsInput(self, resources, personsLeft):
        finished = False
        while not finished:
            try:
                inputString = input(self.prompt % (suffix(resources), str(resources), personsLeft, suffix(personsLeft), suffix(personsLeft))).lower()
                resource, number = inputString[:1], int(inputString[1:])
                finished = True
            except ValueError:
                print("'%s' do not seem to be a number!" % inputString[1:])
        return (resource, number)

    def processPlacePersonsInput(self, resourcePersonCount, playerAbr, board):
        resource, personCount = resourcePersonCount
        if   resource == "f": board.addHunters(personCount, playerAbr)
        elif resource == "w": board.addLumberjacks(personCount, playerAbr)
        elif resource == "c": board.addClayDiggers(personCount, playerAbr)
        elif resource == "s": board.addStoneDiggers(personCount, playerAbr)
        elif resource == "g": board.addGoldDiggers(personCount, playerAbr)
        elif resource == "h": board.placeOnHut(board.availableHuts()[personCount-1], playerAbr)

    def buyHuts(self, player, huts):
        result = [] 
        print("You have placed on following hut%s: " % suffix(huts) + " ".join(hut.asString() for hut in huts))
        nonFood = player.getNonFood()
        print("available resource%s: %s " % (suffix(nonFood), str(nonFood)))
        
        notPayable, payable = self.groupByPayable(player, huts)
        if notPayable:
            print("you can't afford the following hut%s: %s" % (suffix(notPayable), ", ".join([hut.asString() for hut in notPayable])))
            
        while payable:
            hut = payable[0]
            inputString = input("do you want to buy this hut: %s ? (Y|n) " % hut.asString())
            if inputString != "n":
                self.buyHut(player, hut)
                result.append(hut)
                payable.remove(hut)
            notPayable, payable = self.groupByPayable(player, payable)
            if notPayable:
                print("you can't afford the following hut%s: %s" % (suffix(notPayable), ", ".join([hut.asString() for hut in notPayable])))
        return result
        
    def groupByPayable(self, player, huts):
        return ([hut for hut in huts if not player.isPayable(hut)], [hut for hut in huts if player.isPayable(hut)])
    
    def buyHut(self, player, hut):
        player.huts.append(hut)
        player.score += self.pay(player, hut)
            
    def pay(self, player, hut):
        if isinstance(hut, AnyHut) or isinstance(hut, CountHut):
            return sum(self.processPayHut(player, self.fetchResourecestoPay(player.getNonFood(), hut)))
        else:
            player.removeResources(hut.costs([]))
            return hut.value()
    
    def fetchResourecestoPay(self, nonFoodResources, hut):
        finished = False
        while not finished:
            promptString = "choose resources (format='445...') to pay the hut: %s\n available resources: %s " % (hut.asString(), str(nonFoodResources))
            inputString = input(promptString)
            inputResources = [int(ch) for ch in inputString]
            try:
                for r in inputResources:
                    nonFoodResources[:].remove(r)
            except ValueError:
                print("Resources %s not available in %s\n" % (inputString, str(nonFoodResources)))
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

    def processPayHut(self, player, inputString):
        costs = [int(ch) for ch in inputString]
        player.removeResources(costs)
        return costs

        
        
        
    
    
    