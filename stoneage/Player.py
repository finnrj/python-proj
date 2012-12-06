'''
Created on Nov 22, 2012

@author: finn
'''

class Player():
    '''
    classdocs
    '''
    resources = []

    def __init__(self):
        pass

    def isPayable(self, hut):
        return hut.missing(self.resources) == []

    def fetchPayableHut(self, ahs):
        for hut in ahs:
            if self.isPayable(hut):
                return hut
        return None
    
    def placePersons(self, board):
#       check huts
        ahs = board.availableHuts()
        payableHut = self.fetchPayableHut(ahs)
        if payableHut is not None:
            board.placeOnHut(payableHut)
            return
#       place on resources
        
            