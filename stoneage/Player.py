'''
Created on Nov 22, 2012

@author: finn
'''
from Toolbox import Toolbox

class Player():
    '''
    classdocs
    '''
    
    maxFoodTrack   = 10
    maxPersonCount = 10
    hungerPenalty  = -10

    def __init__(self, color, strategy):
        self.resources = 12 * [2]
        self.huts = []
        self.personCount = 5
        self.score = 0
        self.color = color
        self.playerAbr = color[:1].lower()
        self.strategy = strategy
        self.foodTrack = 0
        self.toolbox = Toolbox()

    def getFoodTrack(self):
        return self.foodTrack

    def getTools(self):
        return self.toolbox.getTools()

    def getPersonCount(self):
        return self.personCount

    def foodMissing(self):
        return max(0, (self.personCount - self.foodTrack) - self.resources.count(2))
    
    def feed(self):
        if self.foodMissing() > 0 :
            self.score += self.hungerPenalty
        for person in range((self.personCount - self.foodTrack) - self.foodMissing()): 
            self.resources.remove(2)

    def getNonFood(self):
        return sorted([resource for resource in self.resources if resource != 2])
    
    def addResources(self, additionalResources):
        while 7 in additionalResources: 
            self.foodTrack = min(self.maxFoodTrack, self.foodTrack + 1)
            additionalResources.remove(7)
        while 8 in additionalResources: 
            self.personCount = min(self.maxPersonCount, self.personCount + 1)
            additionalResources.remove(8)
        while 9 in additionalResources: 
            self.toolbox.upgrade()
            additionalResources.remove(9)
        self.resources.extend(additionalResources)
        
    def removeResources(self, resourcesToRemove):
        for resource in resourcesToRemove:
            self.resources.remove(resource)
        
    def buyHuts(self, huts):
        return self.strategy.buyHuts(self, huts)

    def buyHut(self, hut, payment):
        self.huts.append(hut)
        self.executeHutPayment(payment)

    def isPayable(self, hut):
        return self.strategy.isPayable(hut, self.resources)

    def executeHutPayment(self, payment):
        self.removeResources(payment)
        self.score += sum(payment)

    def personsLeft(self, board):
        return self.personCount - board.personCount(self.playerAbr)

    def isNewRound(self, board):
        return self.personsLeft(board) == self.personCount

    def placePersons(self, board):
        self.strategy.placePersons(self, board)
    
    def finalScore(self):
        return self.score + len(self.resources)
    
    def getColor(self):
        return self.color

    def getAbr(self):
        return self.playerAbr
    
    def toolsToUse(self, resourceValue, eyes):
        return self.strategy.toolsToUse(resourceValue, eyes, self.toolbox)
    
    def getStrategy(self):
        return self.strategy
    
    def __str__(self):
        return """People: %d, Foodtrack: %d, Food: %d, Tools: %s
Resources: %s
huts: %s    
score: %d\n""" % (self.getPersonCount(), self.getFoodTrack(), self.resources.count(2), self.toolbox, 
                  str(sorted(self.getNonFood())), 
                  ",". join([hut for hut in self.huts]), self.score)

    
    
    

    
    
    


