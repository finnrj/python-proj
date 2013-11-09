from Hut import AnyHut, CountHut, SimpleHut
from Board import PlacementError

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
    
    def __init__(self):
        self.plannedCosts = {}
    
    def placePersons(self, player, board):
        if player.isNewRound(board):
            self.plannedCosts = {}
        
        # check village 
        if not board.farmOccupied():
            board.placeOnFarm(player.getAbr())
            return
        if not board.breedingHutOccupied() and player.personsLeft(board) > 1:
            board.placeOnBreedingHut(player.getAbr())
            return
        if not board.toolSmithOccupied():
            board.placeOnToolSmith(player.getAbr())
            return
    
        # check huts
        payableHut = self.fetchPayableHut(board.availableHuts(), player.resources[:])
        if payableHut is not None:
            board.placeOnHut(payableHut, player.getAbr())
            self.adjustResources(payableHut, player.resources[:])
            return
        # place on resources
        if player.resources.count(3) < 2 and board.freeForestSlots() > 0:
            board.addLumberjacks(min(player.personsLeft(board), board.freeForestSlots()) , player.getAbr())
        elif player.resources.count(4) < 2 and board.freeClayPitSlots() > 0:
            board.addClayDiggers(min(player.personsLeft(board), board.freeClayPitSlots()), player.getAbr())
        elif player.resources.count(5) < 2 and board.freeQuarrySlots() > 0:
            board.addStoneDiggers(min(player.personsLeft(board), board.freeQuarrySlots()), player.getAbr())
        elif board.freeRiverSlots() > 0:
            board.addGoldDiggers(min(player.personsLeft(board), board.freeRiverSlots()), player.getAbr())
        else:
            board.addHunters(player.personsLeft(board), player.getAbr())
        
    def buyHuts(self, player, huts):
        for hut, payment in self.plannedCosts.items():
            player.buyHut(hut, payment)
        return huts

    def isPayable(self, hut, resources):
        return hut.missing(self.usableResources(resources)) == []

    def fetchPayableHut(self, availableHuts, resources):
        for hut in availableHuts:
            if self.isPayable(hut, resources):
                return hut
        return None
    
    def adjustResources(self, hut, resources):
        self.plannedCosts[hut] = hut.costs(self.usableResources(resources))
        
    def usableResources(self, resources):
        usableResources = resources[:]
        plannedResources = [cost for costs in self.plannedCosts.values() for cost in costs]
        
        for resource in plannedResources:
            usableResources.remove(resource)
        return sorted(usableResources)
    

    def findToolsToKeep(self, unusedTools, greedyToolvalue):
        if unusedTools[0] == greedyToolvalue:
            return unusedTools[1:]
        
        sumToReduce = sum(unusedTools)
        toolsToKeep = []
        for tool in unusedTools:
            if sumToReduce - tool >= greedyToolvalue:
                toolsToKeep.append(tool)
                sumToReduce -= tool
        return toolsToKeep


    def useTools(self, toolbox, toolsToKeep):
        sumToUse = 0
        for tool in toolbox.getUnused():
            if tool in toolsToKeep:
                toolsToKeep.remove(tool)
            else:
                toolbox.use(tool)
                sumToUse += tool
        return sumToUse

    def toolsToUse(self, resourceValue, eyes, toolbox):
        mod = eyes % resourceValue
        greedyToolvalue = resourceValue - mod

        # if tools can't help: quit
        if sum(toolbox.getUnused()) < greedyToolvalue:
            return 0
        
        while sum(toolbox.getUnused()) >= greedyToolvalue + resourceValue:
            greedyToolvalue += resourceValue

        # looking for tools that can be kept
        # precondition: Tools are sorted descending 
        toolsToKeep = self.findToolsToKeep(toolbox.getUnused(), greedyToolvalue)
        return self.useTools(toolbox, toolsToKeep)          

    def chooseReapingResource(self, occupiedResources):
        return occupiedResources[-1]
    
    def chooseChristmas(self, player, presents):
        target = 7 if (presents.count(7) > 0) else max(presents)
        presents.remove(target)
        player.addResources([target])
        return presents

    def __str__(self):
        return "Stupid Bot"
    
class Human(Strategy):
    """Class for a human redPlayer"""
    
    prompt = """You have %d people, foodtrack: %d, food: %d 
and the following resource%s: %s 
%d person%s available. Please place person%s!
"""
     
#        Input format: <resource> <number>, where
#
#            Grounds:                
#                Hunting:   f
#                Forest :   w
#                Clay:      c
#                Quarry:    s
#                River:     g
#                Farm:      a
#                Breeding:  b
#                Toolsmith: t
#            and 'number' the number of persons to
#            place in the chosen ground. 
#
#            Hut: h
#            and 'number' is the index of the hut (1-4)
#            
#    """
   
    def placePersons(self, player, board):
        personsLeft = player.personsLeft(board)
        try:
            resource, number = self.fetchPlacePersonsInput(player.getPersonCount(), player.getFoodTrack(), player.resources.count(2),
                                                           player.getNonFood(), personsLeft)
            if not resource in "hfwcsgabt":
                raise PlacementError("illegal character:"+resource)
            elif resource == "b" and personsLeft < 2:
                raise PlacementError("cannot breed with only %d person left" % (personsLeft))
            elif resource != "h" and number > personsLeft:
                raise PlacementError("cannot place %d persons with only %d left" % (number, personsLeft))
            elif resource == "h" and  number > 4:
                raise PlacementError("hut index has be between 1 - 4, not %d" % (number))
            self.processPlacePersonsInput(resource, number, player.getAbr(), board)
        except PlacementError as e:
            print("ERROR: " + str(e) + "\n")
            print (board)
            self.placePersons(player, board)
    
    def fetchPlacePersonsInput(self, people, foodtrack, food, resources, personsLeft):
        return fetchConvertedInput(self.prompt % (people, foodtrack, food, suffix(resources), str(resources), personsLeft, suffix(personsLeft), 
                                   suffix(personsLeft)),
                                   lambda v: printfString("'%s' does not seem to be of format <resource><number>!", v),
                                   stringAndNumber)
        
    def processPlacePersonsInput(self, resource, number, playerAbr, board):
        if   resource == "f": board.addHunters(number, playerAbr)
        elif resource == "w": board.addLumberjacks(number, playerAbr)
        elif resource == "c": board.addClayDiggers(number, playerAbr)
        elif resource == "s": board.addStoneDiggers(number, playerAbr)
        elif resource == "g": board.addGoldDiggers(number, playerAbr)
        elif resource == "a": board.placeOnFarm(playerAbr)
        elif resource == "b": board.placeOnBreedingHut(playerAbr)
        elif resource == "t": board.placeOnToolSmith(playerAbr)
        elif resource == "h": board.placeOnHutIndex(number - 1, playerAbr)

    def printResourceStatus(self, player):
        nonFood = player.getNonFood()
        print("available resource%s: %s " % (suffix(nonFood), str(nonFood)))

    def buyHuts(self, player, huts):
        if huts:
            print("You have placed on following hut%s: " % suffix(huts) + " ".join(str(hut) for hut in huts))
        return self.doBuyHuts(player, self.filterOutPayableHuts(player, huts), [])
    
    def doBuyHuts(self, player, payableHuts, boughtHuts):
        if not payableHuts:
            return boughtHuts
        else:
            self.printResourceStatus(player)
            hut = payableHuts.pop()
            if self.wantsToBuy(hut):
                self.buyHut(player, hut)
                boughtHuts.append(hut)
            return self.doBuyHuts(player, self.filterOutPayableHuts(player, payableHuts), boughtHuts)
        
    def wantsToBuy(self, hut):
        return fetchConvertedInput("do you want to buy this hut: %s ? (y|n) " % str(hut),
                                   lambda v: printfString("please answer y(es) or n(o) - not: '%s'", v),
                                   yesNo) 
        
    def filterOutPayableHuts(self, player, huts):
        notPayable, payable = [hut for hut in huts if not player.isPayable(hut)], [hut for hut in huts if player.isPayable(hut)]
        if notPayable:
            print("you can't afford the following hut%s: %s" % (suffix(notPayable), " ".join([str(hut) for hut in notPayable])))
        return payable

    def isPayable(self, hut, resources):
        return hut.missing(resources) == []
    
    def buyHut(self, player, hut):
        if isinstance(hut, SimpleHut):
            player.buyHut(hut, hut.costs([]))
        else:  # CountHut or AnyHut
            player.buyHut(hut, self.chooseResourecestoPay(player.getNonFood(), hut))
            
    def chooseResourecestoPay(self, nonFoodResources, hut):
        promptString = "\nchoose resources (format='445...') to pay the hut: %s\n available resources: %s " % (str(hut), str(nonFoodResources))

        finished = False
        while not finished:
            chosenResources = fetchConvertedInput(promptString,
                                                 lambda v: printfString("the input '%s' does not consist of only numbers!", v),
                                                 mapToNumbers)
            finished = all([self.chosenItemsAvailable(nonFoodResources, chosenResources),
                            self.validPaymentIfAnyHut(hut, chosenResources),
                            self.validPaymentIfCountHut(hut, chosenResources)])
        return chosenResources

    def chosenItemsAvailable(self, available, chosen):
        try:
            clone = available[:]
            for r in chosen:
                clone.remove(r)
            return True
        except ValueError:
            print("Items %s not available in %s\n" % (str(chosen), str(available)))
            return False
        
    def validPaymentIfAnyHut(self, hut, payment):
        if not isinstance(hut, AnyHut):
            return True
        if len(payment) == 0:
            print("please pay something!")
        if len(payment) >= 8:
            print("too much payment! (%d resources) Maximal 7 resources please" % len(payment))
        return len(payment) > 0 and len(payment) < 8

    def validPaymentIfCountHut(self, hut, payment):
        if not isinstance(hut, CountHut):
            return True
        if len(hut.missing(payment)) != 0:
            print("missing resources: " + str(hut.missing(payment)))
        if len(payment) != hut.getResourceCount():
            print("Given resource count:" + str(len(payment)) + ", required count: " + str(hut.getResourceCount()))
        return len(hut.missing(payment)) == 0 and len(payment) == hut.getResourceCount()
    
    def toolsToUse(self, resourceValue, eyes, toolbox):
        mod = eyes % resourceValue
        unusedTools = toolbox.getUnused()
        if mod + sum(unusedTools) < resourceValue:
            return 0
        else:
            promptString = """\nResourcevalue: %d, eyes: %d, your available tools: %s
            choose tools to use (format='2', '21', '221') """ % (resourceValue, eyes, str(unusedTools))
            finished = False
            while not finished:
                chosenTools = fetchConvertedInput(promptString,
                                                 lambda v: printfString("the input '%s' does not consist of only numbers!", v),
                                                 mapToNumbers)
                finished = self.chosenItemsAvailable(unusedTools, chosenTools)
            self.useTools(toolbox, chosenTools[:])
            return sum(chosenTools)
    
    def useTools(self, toolbox, toolsToUse):
        for tool in toolbox.getUnused():
            if tool in toolsToUse:
                toolbox.use(tool)
                toolsToUse.remove(tool)

    def chooseReapingResource(self, occupiedResources):
        promptString = """\nWhich Resource to Reap? (%s) """ % (occupiedResources)
        if len(occupiedResources) == 1:
            return occupiedResources[0]
        finished = False 
        while not finished:
            chosenResource = input(promptString).lower()
            finished = chosenResource and chosenResource in occupiedResources
            if not finished:
                print("'%s' not in '%s'" % (chosenResource, occupiedResources))
        return chosenResource

    def chooseChristmas(self, player, presents):
        promptString = """\nChoose resource for Christmas from (%s) """ % (presents)
        finished = False
        while not finished:
            chosenResource = mapToNumbers(input(promptString).lower())[0]
            finished = chosenResource and chosenResource in presents
            if not finished:
                print("'%s' not in '%s'" % (chosenResource, presents))
        presents.remove(chosenResource)
        player.addResources([chosenResource])
        return presents

    def __str__(self):
        return "Human"



# output helper methods 
def suffix(numberOrList):
    size = numberOrList if isinstance(numberOrList, type(1)) else len(numberOrList)
    return "s" if size > 1 or size == 0 else ""

def yesNo(inputString):
    yesNoDict = {"y" : True, "n" : True}
    return yesNoDict[inputString.lower()[0]]
    
def stringAndNumber(inputString):
    return (inputString[:1], abs(int(inputString[1:])))

def mapToNumbers(inputString):
    return [int(ch) for ch in inputString]

def printfString(string, values):
    return string % values

def fetchConvertedInput(promptMsg, errorMsgFunc, convertFunc):
    inputString = input(promptMsg).lower()
    finished = False
    while not finished:
        try:
            result = convertFunc(inputString)
            finished = True
        except:
            print(errorMsgFunc(inputString))
            inputString = input(promptMsg).lower()
    return result
    
    
    
