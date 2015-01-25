'''
Created on Nov 22, 2012

@author: finn
'''

from functools import total_ordering
from enum import Enum

from Toolbox import Toolbox
from Card import SymbolCard, MultiplierCard, CardMultiplier
from Resource import Resource

class PlayerColor(Enum):
    '''background colors for player persons'''
    
    Red = '\x1b[48;5;9m'
    Green = '\x1b[42m'
    Yellow = '\x1b[48;5;11m'
    Blue = '\x1b[48;5;33m'
# foreground colors
#     Red = '\x1b[1;31m'
#     Green = '\x1b[1;32m'
#     Yellow = '\x1b[2;33m'
#     Blue = '\x1b[1;34m'

@total_ordering
class Player():
    '''
    classdocs
    '''
    
    maxFoodTrack   = 10
    maxPersonCount = 10
    hungerPenalty  = -10
    colorOSnormal  = '\x1b[0m'

    def __init__(self, color, strategy):
        self.joker = 12 * [Resource.food]
        self.huts = []
        self.cards = []
        self.person = 5
        self.point = 0
        self.color = color
        self.playerAbr = color.name[:1].lower()
        self.colorOS = color.value
        self.strategy = strategy
        self.foodtrack = 0
        self.toolbox = Toolbox()
        self.oneTimeTools = []
        
    def __lt__(self, other):
        if self.getScore() != other.getScore():
            return self.getScore() < other.getScore()
        return  self.secondScoreCriteria() < other.secondScoreCriteria()  

    def __eq__(self, other):
        return self is other
    
    def __hash__(self):
        return hash("".join([o.__str__() for o in [self.getColor(), self.strategy]]))

    def getFoodTrack(self):
        return self.foodtrack

    def getTools(self):
        return self.toolbox.getTools()

    def getPersonCount(self):
        return self.person

    def foodMissing(self):
        return max(0, (self.person - self.foodtrack) - self.joker.count(Resource.food))
    
    def feed(self):
        if self.foodMissing() > 0 :
            self.point += self.hungerPenalty
        for person in range((self.person - self.foodtrack) - self.foodMissing()): 
            self.joker.remove(Resource.food)

    def getFood(self):
        return [resource for resource in self.joker if resource == Resource.food]
    
    def getNonFood(self):
        return sorted([resource for resource in self.joker if resource != Resource.food])

    def addResources(self, additionalResources):
        while Resource.tool in additionalResources: 
            self.toolbox.upgrade()
            additionalResources.remove(Resource.tool)
        while Resource.foodtrack in additionalResources: 
            self.foodtrack = min(self.maxFoodTrack, self.foodtrack + 1)
            additionalResources.remove(Resource.foodtrack)
        while Resource.person in additionalResources: 
            self.person = min(self.maxPersonCount, self.person + 1)
            additionalResources.remove(Resource.person)
        self.joker.extend(additionalResources)
        
    def addOneTimeTool(self, value):
        self.oneTimeTools.append(value)
        
    def removeResources(self, resourcesToRemove):
        for resource in resourcesToRemove:
            self.joker.remove(resource)
        
    def buyHuts(self, huts):
        return self.strategy.buyHuts(self, huts)

    def buyHut(self, hut, payment):
        self.huts.append(hut)
        self.executeHutPayment(payment)

    def isPayable(self, hut):
        return self.strategy.isPayable(hut, self.joker)

    def executeHutPayment(self, payment):
        self.removeResources(payment)
        self.point += sum(payment)

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
            if card.getSymbol() == CardMultiplier.hutcount:
                mulitplierPoints += card.getMultiplier() * len(self.huts)
            elif card.getSymbol() == CardMultiplier.foodtrack:
                mulitplierPoints += card.getMultiplier() * self.foodtrack
            elif card.getSymbol() == CardMultiplier.toolsum:
                mulitplierPoints += card.getMultiplier() * sum(self.toolbox.getTools())
            elif card.getSymbol() == CardMultiplier.personcount:
                mulitplierPoints += card.getMultiplier() * self.person

        return points1 + points2 + mulitplierPoints
       
    def addScore(self, score):
        self.point += score

    def getScore(self):
        return self.point + self.getCardScore() + len(self.getNonFood())
    
    def secondScoreCriteria(self):
        return self.foodtrack + sum(self.toolbox.getTools()) + self.person
    
    def personsLeft(self, board):
        return self.person - board.person(self)

    def isNewRound(self, board):
        return self.personsLeft(board) == self.person

    def placePersons(self, board):
        self.strategy.placePersons(self, board)
        
    def chooseChristmas(self, presents):
        return self.strategy.chooseChristmas(self, presents)
    
    def getColor(self):
        return self.color

    def getOutputColor(self, length = None):
        actualLength = length if length else len(self.color.name)
        nameString = "%-" + str(actualLength) + "s"
        return ("%s" + nameString + "%s") %  (self.colorOS, self.color.name, self.colorOSnormal)

    def getAbr(self):
        return self.playerAbr

    def getOutputAbr(self):
        return "%s%s%s" %  (self.colorOS, self.playerAbr, self.colorOSnormal)
    
    def toolsToUse(self, resource, eyes): 
        return self.strategy.toolsToUse(resource, eyes, self.toolbox, self.oneTimeTools)
    
    def newRound(self):
        self.toolbox.reset()
    
    def getStrategy(self):
        return self.strategy
    
    def chooseReapingResource(self, occupiedResources):
        return self.strategy.chooseReapingResource(occupiedResources)
    
    def resourcesColoredOutput(self):
        return "[%s]" % ",".join([resource.getColoredName() for resource in sorted(self.getNonFood())])
    
    def __str__(self):
        return """%s%s%s
People: %d, Foodtrack: %d, Food: %d, Tools: %s, One-time tools: %s
Resources: %s
Hutcount: %d    
score (cardscore): %d (%d)\n""" % (self.colorOS, self.color.name, self.colorOSnormal, \
                  self.getPersonCount(), self.getFoodTrack(), self.joker.count(Resource.food), self.toolbox, self.oneTimeTools,  
                  Resource.coloredOutput(sorted(self.getNonFood())), 
                  len(self.huts), \
                  self.getScore(), self.getCardScore())

