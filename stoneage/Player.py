'''
Created on Nov 22, 2012

@author: finn
'''

class Player():
    '''
    classdocs
    '''

    def __init__(self):
        self.resources = 12 * [2]
        self.plannedCosts = []
        self.huts = []
        self.personCount = 5
        self.score = 0

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
    
    def placePersons(self, board):
        self.plannedCosts = []
        
        if board.personCount() == self.personCount:
            return
        # check huts
        payableHut = self.fetchPayableHut(board.availableHuts())
        if payableHut is not None:
            board.placeOnHut(payableHut)
            self.adjustResources(payableHut.costs(self.resources))
            return
        # place on resources
        if self.resources.count(3) < 2:
            board.addLumberjacks(self.personCount - board.personCount())
        elif self.resources.count(4) < 2:
            board.addClayDiggers(self.personCount - board.personCount())
        elif self.resources.count(5) < 2:
            board.addStoneDiggers(self.personCount - board.personCount())
        else:
            board.addGoldDiggers(self.personCount - board.personCount())
            
    def toString(self):
        return """Resources: %s
huts: %s
score: %d""" % (str(self.resources), ",". join([hut.toString() for hut in self.huts]), self.score)
