'''
Created on Nov 22, 2012

@author: finn
'''

class Player():
    '''
    classdocs
    '''

    def __init__(self):
        self.resources = []
        self.plannedCosts = []
        self.personCount = 5

    def isPayable(self, hut):
        return hut.missing(self.resources) == []

    def fetchPayableHut(self, avaiableHuts):
        for hut in avaiableHuts:
            if self.isPayable(hut):
                return hut
        return None
    
    def addResources(self, additionalResources):
        self.resources.extend(additionalResources)
        
    def adjustResources(self, costs):
        for cost in costs:
            self.resources.remove(cost)
            self.plannedCosts.append(cost)
    
    def placePersons(self, board):
        if board.personCount() == self.personCount:
            return
#       check huts
        payableHut = self.fetchPayableHut(board.availableHuts())
        if payableHut is not None:
            board.placeOnHut(payableHut)
            self.adjustResources(payableHut.costs())
            return
#       place on resources
        if self.resources.count(3) < 2:
            board.addLumberjacks(self.personCount - board.personCount())
            