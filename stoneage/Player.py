'''
Created on Nov 22, 2012

@author: finn
'''
from Toolbox import Toolbox
from Card import SymbolCard, MultiplierCard

class Player():
    '''
    classdocs
    '''
    
    maxFoodTrack   = 10
    maxPersonCount = 10
    hungerPenalty  = -10
    colorOSnormal  = '\033[0m'

    def __init__(self, color, strategy):
        self.resources = 12 * [2]
        self.huts = []
        self.cards = []
        self.personCount = 5
        self.score = 0
        self.color = color
        self.playerAbr = color[:1].lower()
        if color == 'Red':
            self.colorOS = '\033[91m'
        elif color == 'Green':
            self.colorOS = '\033[92m'
        elif color == 'Yellow':
            self.colorOS = '\033[93m'
        elif color == 'Blue':
            self.colorOS = '\033[94m'
        else:
            self.colorOS = self.colorOSnormal
        self.strategy = strategy
        self.foodTrack = 0
        self.toolbox = Toolbox()
        self.oneTimeTools = []

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

    def getFood(self):
        return [resource for resource in self.resources if resource == 2]
    
    def getNonFood(self):
        return sorted([resource for resource in self.resources if resource != 2])

    def addResources(self, additionalResources):
        while 7 in additionalResources: 
            self.toolbox.upgrade()
            additionalResources.remove(7)
        while 8 in additionalResources: 
            self.foodTrack = min(self.maxFoodTrack, self.foodTrack + 1)
            additionalResources.remove(8)
        while 9 in additionalResources: 
            self.personCount = min(self.maxPersonCount, self.personCount + 1)
            additionalResources.remove(9)
        self.resources.extend(additionalResources)
        
    def addOneTimeTool(self, value):
        self.oneTimeTools.append(value)
        
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

    def addCard(self, card, players, cardPile):
        self.cards.append(card)
        card.execute(players, cardPile)
   
    def getCardScore(self):
        symbolList = {}
        for card in [c for c in self.cards if isinstance(c, SymbolCard)]:
            if not card.getSymbol() in symbolList.keys():
                symbolList[card.getSymbol()] = []
            symbolList[card.getSymbol()].append(card)
        
        points1 = pow(len(symbolList.keys()), 2)
        points2 = pow(len([lst for lst in symbolList.values() if len(lst) == 2]), 2)
        
        mulitplierPoints = 0
        for card in [c for c in self.cards if isinstance(c, MultiplierCard)]:
            if card.getSymbol() == "hutBuilder":
                mulitplierPoints += card.getMultiplier() * len(self.huts)
            elif card.getSymbol() == "farmer":
                mulitplierPoints += card.getMultiplier() * self.foodTrack
            elif card.getSymbol() == "toolMaker":
                mulitplierPoints += card.getMultiplier() * sum(self.toolbox.getTools())
            elif card.getSymbol() == "shaman":
                mulitplierPoints += card.getMultiplier() * self.personCount

        return points1 + points2 + mulitplierPoints
       
    def addScore(self, score):
        self.score += score

    def getScore(self):
        return self.score
    
    def personsLeft(self, board):
        return self.personCount - board.personCount(self.playerAbr)

    def isNewRound(self, board):
        return self.personsLeft(board) == self.personCount

    def placePersons(self, board):
        self.strategy.placePersons(self, board)
        
    def chooseChristmas(self, presents):
        return self.strategy.chooseChristmas(self, presents)
    
    def finalScore(self):
        return self.score + len(self.resources)
    
    def getColor(self):
        return self.color

    def getColorForOutput(self):
        return "%s%-5s%s" %  (self.colorOS, self.color, self.colorOSnormal)

    def getAbr(self):
        return self.playerAbr
    
    def toolsToUse(self, resourceValue, eyes): 
        return self.strategy.toolsToUse(resourceValue, eyes, self.toolbox)
    
    def newRound(self):
        self.toolbox.reset()
    
    def getStrategy(self):
        return self.strategy
    
    def chooseReapingResource(self, occupiedResources):
        return self.strategy.chooseReapingResource(occupiedResources)
    
    def __str__(self):
        return """%sPeople: %d, Foodtrack: %d, Food: %d, Tools: %s
Resources: %s
huts: %s    
score: %d%s\n""" % (self.colorOS, self.getPersonCount(), self.getFoodTrack(), self.resources.count(2), self.toolbox, 
                  str(sorted(self.getNonFood())), 
                  ",".join([str(hut) for hut in self.huts]), self.score, self.colorOSnormal)

    
    
    

    
    
    

    
    
    

    
    
    


