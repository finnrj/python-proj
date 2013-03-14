'''
Created on Nov 22, 2012

@author: finn
'''

class Player():
    '''
    classdocs
    '''

    def __init__(self, color):
        self.resources = 12 * [2]
        self.plannedCosts = []
        self.huts = []
        self.personCount = 5
        self.score = 0
        self.color = color
        self.abr = color[:1].lower()

    def foodMissing(self):
        return max(0, self.personCount - self.resources.count(2))
    
    def feed(self):
        if self.foodMissing() > 0 :
            self.score -= 10
        for person in range(self.personCount - self.foodMissing()): 
            self.resources.remove(2)

    def isPayable(self, hut):
        return hut.missing(self.resources) == []

    def fetchPayableHut(self, availableHuts):
        for hut in availableHuts:
            if self.isPayable(hut):
                return hut
        return None
    
    def addResources(self, additionalResources):
        self.resources.extend(additionalResources)
        
    def addHuts(self, boughtHuts):
        self.huts.extend(boughtHuts)
        self.score += sum([hut.value() for hut in boughtHuts])
        
    def adjustResources(self, costs):
        for cost in costs:
            self.resources.remove(cost)
            self.plannedCosts.append(cost)
    
    def personsLeft(self, board):
        return self.personCount - board.personCount(self.abr)

    def placePersons(self, board):
        self.plannedCosts = []
        
        if board.personCount(self.abr) == self.personCount:
            return
        # check huts
        payableHut = self.fetchPayableHut(board.availableHuts())
        if payableHut is not None:
            board.placeOnHut(payableHut, self.abr)
            self.adjustResources(payableHut.costs(self.resources))
            return
        # place on resources
        if self.resources.count(3) < 2 and board.freeForestSlots() > 0:
            board.addLumberjacks(min(self.personsLeft(board), board.freeForestSlots()) , self.abr)
        elif self.resources.count(4) < 2 and board.freeClayPitSlots() > 0:
            board.addClayDiggers(min(self.personsLeft(board), board.freeClayPitSlots()), self.abr)
        elif self.resources.count(5) < 2 and board.freeQuarrySlots() > 0:
            board.addStoneDiggers(min(self.personsLeft(board), board.freeQuarrySlots()), self.abr)
        elif board.freeRiverSlots() > 0:
            board.addGoldDiggers(min(self.personsLeft(board), board.freeRiverSlots()), self.abr)
        else:
            board.addHunters(self.personsLeft(board), self.abr)
    
    def finalScore(self):
        return self.score + len(self.resources)
    
    def getColor(self):
        return self.color

    def getAbr(self):
        return self.abr
    
    def toString(self):
        return """Resources: %s
huts: %s    
score: %d""" % (str(self.resources), ",". join([hut.toString() for hut in self.huts]), self.score)
