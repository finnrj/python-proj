from Hut import AnyHut, CountHut, SimpleHut
from Board import PlacementError
from Resource import Resource

ERROR_PREFIX = '\x1b[1;33m\x1b[45m'
ERROR_SUFFIX = '\x1b[0m'

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

    def isPayable(self, hut, resources):
        return hut.missing(resources) == []
    
class StupidBot(Strategy):
    
    def __init__(self):
        self.plannedCosts = {}
        
    def placePersons(self, player, board):
        if player.isNewRound(board):
            self.plannedCosts = {}
        
        # check village 
        if not board.farmOccupied():
            board.placeOnFarm(player)
            return
        if not board.breedingHutOccupied() and player.personsLeft(board) > 1:
            board.placeOnBreedingHut(player)
            return
        if not board.toolSmithOccupied():
            board.placeOnToolSmith(player)
            return
    
        # check huts
        payableHut = self.fetchPayableHut(board.availableHuts(), player.joker[:])
        if payableHut is not None:
            board.placeOnHut(payableHut, player)
            self.updatePlannedCosts(payableHut, player.joker[:])
            return
        # place on resources
        if player.joker.count(Resource.wood) < 2 and board.freeForestSlots() > 0:
            board.addLumberjacks(min(player.personsLeft(board), board.freeForestSlots()) , player)
        elif player.joker.count(Resource.clay) < 2 and board.freeClayPitSlots() > 0:
            board.addClayDiggers(min(player.personsLeft(board), board.freeClayPitSlots()), player)
        elif player.joker.count(Resource.stone) < 2 and board.freeQuarrySlots() > 0:
            board.addStoneDiggers(min(player.personsLeft(board), board.freeQuarrySlots()), player)
        elif board.freeRiverSlots() > 0:
            board.addGoldDiggers(min(player.personsLeft(board), board.freeRiverSlots()), player)
        else:
            board.addHunters(player.personsLeft(board), player)
        
    def buyHuts(self, player, huts):
        for hut, payment in self.plannedCosts.items():
            player.buyHut(hut, payment)
        return huts

    def fetchPayableHut(self, availableHuts, resources):
        nonPlannedResources = self.nonPlannedResources(resources)
        for hut in availableHuts:
            if self.isPayable(hut, nonPlannedResources):
                return hut
        return None
    
    def updatePlannedCosts(self, hut, resources):
        self.plannedCosts[hut] = hut.costs(self.nonPlannedResources(resources))
        
    def nonPlannedResources(self, resources):
        usableResources = resources[:]
        plannedResources = [cost for costs in self.plannedCosts.values() for cost in costs]
        
        for resource in plannedResources:
            usableResources.remove(resource)
        return sorted(usableResources)
    

    def findToolsToKeep(self, unusedTools, greedyToolvalue):
        if len(unusedTools) == 0:
            return unusedTools
        
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

    def useOneTimeTools(self, resource, greedyToolvalue, oneTimeTools):
        oneTimeValueToUse = 0
        if greedyToolvalue in oneTimeTools:
            oneTimeValueToUse += greedyToolvalue
            oneTimeTools.remove(greedyToolvalue)
        elif (greedyToolvalue + resource) in oneTimeTools:
            oneTimeValueToUse += greedyToolvalue + resource
            oneTimeTools.remove(greedyToolvalue + resource)
        return oneTimeValueToUse

    def toolsToUse(self, resource, eyes, toolbox, oneTimeTools):
        mod = eyes % resource
        greedyToolvalue = resource - mod

        # if tools can't help: quit
        if sum(toolbox.getUnused() + oneTimeTools) < greedyToolvalue:
            return 0

        oneTimeValueToUse = self.useOneTimeTools(resource, greedyToolvalue, oneTimeTools)
        
        while sum(toolbox.getUnused()) >= greedyToolvalue + resource:
            greedyToolvalue += resource

        # looking for tools that can be kept
        # precondition: Tools are sorted descending 
        toolsToKeep = self.findToolsToKeep(toolbox.getUnused(), greedyToolvalue)
        return self.useTools(toolbox, toolsToKeep) + oneTimeValueToUse

    def chooseReapingResource(self, occupiedResources):
        return occupiedResources[-1]
    
    def chooseChristmas(self, player, presents):
        target = max(presents)
        presents.remove(target)
        player.addResources([target])
        return presents

    def __str__(self):
        return "Stupid Bot"
    
class Human(Strategy):
    """Class for a human player"""
    
    prompt = """You have %d people, foodtrack: %d, food: %d 
and the following Resource%s: %s 
%d person%s available. Please place person%s!
"""
     
#        Input format: <Resource> <number>, where
#
#            Grounds:                
#                Hunting:   f
#                Forest :   w
#                Clay:      c
#                Quarry:    s
#                River:     g
#                Toolsmith: t
#                Farm:      a
#                Breeding:  b
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
            resource, number = self.fetchPlacePersonsInput(player.getPersonCount(), player.getFoodTrack(), player.joker.count(Resource.food), player.getNonFood(), personsLeft)
            if not resource in "hfwcsgtab":
                raise PlacementError("illegal character: "+resource)
            elif resource not in "tab" and number == 0:
                raise PlacementError("please place at least one person")
            elif resource == "b" and personsLeft < 2:
                raise PlacementError("cannot breed with only %d person left" % (personsLeft))
            elif resource != "h" and number > personsLeft:
                raise PlacementError("cannot place %d persons with only %d left" % (number, personsLeft))
            elif resource == "h" and  number > 4:
                raise PlacementError("hut index has to be between 1 - 4, not %d" % (number))
            self.processPlacePersonsInput(resource, number, player, board)
        except PlacementError as e:
            printError("ERROR: " + str(e))
            print (board)
            self.placePersons(player, board)
    
    def fetchPlacePersonsInput(self, people, foodtrack, food, resources, personsLeft):
        return fetchConvertedInput(self.prompt % (people, foodtrack, food, suffix(resources), Resource.coloredOutput(resources), personsLeft, suffix(personsLeft), suffix(personsLeft)),
                                   lambda v: printfString("'%s' does not seem to be of format <Resource><number>!", v),
                                   stringAndNumber)
        
    def processPlacePersonsInput(self, resource, number, player, board):
        if   resource == "f": board.addHunters(number, player)
        elif resource == "w": board.addLumberjacks(number, player)
        elif resource == "c": board.addClayDiggers(number, player)
        elif resource == "s": board.addStoneDiggers(number, player)
        elif resource == "g": board.addGoldDiggers(number, player)
        elif resource == "t": board.placeOnToolSmith(player)
        elif resource == "a": board.placeOnFarm(player)
        elif resource == "b": board.placeOnBreedingHut(player)
        elif resource == "h": board.placeOnHutIndex(number - 1, player)

    def printResourceStatus(self, player):
        nonFood = player.getNonFood()
        print("available Resource%s: %s " % (suffix(nonFood), Resource.coloredOutput(nonFood)))

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
        return fetchConvertedInput("do you want to buy this hut (y|n): %s ? (y) " % str(hut),
                                   lambda v: printfString("please answer y(es) or n(o) - not: '%s'", v),
                                   yesNo) 
        
    def filterOutPayableHuts(self, player, huts):
        notPayable, payable = [hut for hut in huts if not player.isPayable(hut)], [hut for hut in huts if player.isPayable(hut)]
        if notPayable:
            printError("you can't afford the following hut%s: " % suffix(notPayable), " ".join([str(hut) for hut in notPayable]))
        return payable

    def buyHut(self, player, hut):
        if isinstance(hut, SimpleHut):
            player.buyHut(hut, hut.costs([]))
        else:  # CountHut or AnyHut
            player.buyHut(hut, self.chooseResourecestoPay(player.getNonFood(), hut))
            
    def chooseResourecestoPay(self, nonFoodResources, hut):
        promptString = "\nchoose resources (format='wcsgj...') to pay the hut: %s\n available resources: %s " % (str(hut), 
                                                                                                                 Resource.coloredOutput(nonFoodResources))

        finished = False
        while not finished:
            chosenResources = fetchConvertedInput(promptString,
                                                 lambda v: printfString("the input '%s' does not consist of only numbers!", v),
                                                 mapToResources)
            if not chosenResources:
                chosenResources = nonFoodResources
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
            printError("Items %s not available in %s\n" % (str(chosen), str(available)))
            return False
        
    def validPaymentIfAnyHut(self, hut, payment):
        if not isinstance(hut, AnyHut):
            return True
        if len(payment) == 0:
            print("please pay something!")
        if len(payment) >= 8:
            printError("too much payment! (%d resources) Maximal 7 resources please" % len(payment))
        return len(payment) > 0 and len(payment) < 8

    def validPaymentIfCountHut(self, hut, payment):
        if not isinstance(hut, CountHut):
            return True
        if len(hut.missing(payment)) != 0:
            printError("missing resources: " + str(hut.missing(payment)))
        if len(payment) != hut.getResourceCount():
            printError("Given Resource count:" + str(len(payment)) + ", required count: " + str(hut.getResourceCount()))
        return len(hut.missing(payment)) == 0 and len(payment) == hut.getResourceCount()
    
    def toolsToUse(self, resourceValue, eyes, toolbox, oneTimeTools):
        mod = eyes % resourceValue
        unusedTools = toolbox.getUnused()
        if sum(unusedTools + oneTimeTools) < resourceValue - mod:
            return 0
        else:
            promptString = """\nResourcevalue: %d, eyes: %d, your available tools: %s, oneTimeTools: %s
            choose tools to use (format='2', '21', '221') """ % (resourceValue, eyes, str(unusedTools), str(oneTimeTools))
            finished = False
            while not finished:
                chosenTools = fetchConvertedInput(promptString,
                                                 lambda v: printfString("the input '%s' does not consist of only numbers!", v),
                                                 mapToNumbers)
                finished = self.chosenItemsAvailable(unusedTools + oneTimeTools, chosenTools)
                
            for tool in chosenTools[:]:
                if not tool in unusedTools:
                    oneTimeTools.remove(tool)
                    chosenTools.remove(tool)
                    
            self.useTools(toolbox, chosenTools[:])
            return sum(chosenTools)
    
    def useTools(self, toolbox, toolsToUse):
        for tool in toolbox.getUnused():
            if tool in toolsToUse:
                toolbox.use(tool)
                toolsToUse.remove(tool)

    def chooseReapingResource(self, occupiedResources):
        firstOccupied = occupiedResources[0]
        if len(occupiedResources) == 1:
            return firstOccupied
        promptString = """\nWhich ResourceField %s to Reap? (%s) """ % (occupiedResources, firstOccupied)
        finished = False 
        while not finished:
            chosenResource = input(promptString).lower()
            finished = chosenResource == None or chosenResource in occupiedResources
            if not finished:
                print("'%s' not in '%s'" % (chosenResource, occupiedResources))
        return chosenResource if chosenResource else firstOccupied

    def chooseChristmas(self, player, presents):
        stringPresents = "%s" % (", ".join([present.name for present in presents]))  
        promptString = """\nChoose Resource for Christmas from %s, index: 1-%d""" % (stringPresents, len(presents))
        finished = False
        while not finished:
            inputString = input(promptString).lower()
            if not inputString:
                inputChar = "1" 
            else: 
                inputChar = inputString[0]

            try:               
                chosenResource = presents[int(inputChar) - 1]
            except:
                chosenResource = None
            finished = inputChar and chosenResource != None
            if not finished:
                print("'%s' not in '%d'" % (inputChar, len(presents)))
        presents.remove(chosenResource)
        player.addResources([chosenResource])
        return presents

    def __str__(self):
        return "Human"

# output helper methods

def printError(errormessage, messageSuffix = None):
    print("%s %s %s %s\n" % (ERROR_PREFIX, errormessage, ERROR_SUFFIX, messageSuffix if messageSuffix else "")) 
    
def suffix(numberOrList):
    size = numberOrList if isinstance(numberOrList, type(1)) else len(numberOrList)
    return "s" if size > 1 or size == 0 else ""

def yesNo(inputString):
    if not inputString : return True
    yesNoDict = {"y" : True, "n" : False}
    return yesNoDict[inputString.lower()[0]]
    
def stringAndNumber(inputString):
    number = abs(int(inputString[1:])) if len(inputString) > 1 else 0
    return (inputString[:1], number)

def mapToNumbers(inputString):
    if not inputString : return []
    return [int(ch) for ch in inputString]

letter2Resource = {'w' : Resource.wood,
                   'c' : Resource.clay,
                   's' : Resource.stone,
                   'g' : Resource.gold,
                   'j' : Resource.joker}

def mapToResources(inputString):
    if not inputString : return []
    return [letter2Resource[ch] for ch in inputString]

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
            printError(errorMsgFunc(inputString))
            inputString = input(promptMsg).lower()
    return result
    
    
    
