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

    def isPayable(self, hut):
        return hut.missing(self.resources) == []

    def fetchPayableHut(self, ahs):
        for hut in ahs:
            if self.isPayable(hut):
                return hut
        return None
    
    def addResources(self, additionalResources):
        self.resources.extend(additionalResources)
    
    def placePersons(self, board):
        if board.personCount() == 5:
            return
#       check huts
        ahs = board.availableHuts()
        payableHut = self.fetchPayableHut(ahs)
        if payableHut is not None:
            board.placeOnHut(payableHut)
            return
#       place on resources
        if self.resources.count(3) < 2:
            board.addLumberjacks(5)
            