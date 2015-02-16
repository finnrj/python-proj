'''
Created on Nov 22, 2012

@author: finn
'''

from functools import total_ordering
from itertools import groupby
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
        self.resources = 12 * [Resource.food]
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
        return max(0, (self.person - self.foodtrack) - self.resources.count(Resource.food))
    
    def feed(self):
        if self.foodMissing() > 0 :
            self.point += self.hungerPenalty
        for person in range((self.person - self.foodtrack) - self.foodMissing()): 
            self.resources.remove(Resource.food)

    def getFood(self):
        return [resource for resource in self.resources if resource == Resource.food]
    
    def getNonFood(self):
        return sorted([resource for resource in self.resources if resource != Resource.food])

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
        self.resources.extend(additionalResources)
        
    def addOneTimeTool(self, value):
        self.oneTimeTools.append(value)
        
    def removeResources(self, resourcesToRemove):
        for resource in resourcesToRemove:
            if resource in self.resources:
                self.resources.remove(resource)
            else:
                print("trying to remove resource: %s from resources: %s" % (resource.name, Resource.coloredOutput(self.resources))) 
        
    def buyHuts(self, huts):
        return self.strategy.buyHuts(self, huts)

    def buyHut(self, hut, payment):
        self.huts.append(hut)
        self.removeResources(payment)
        self.point += sum(payment)

    def buyCards(self, cards, players, cardPile):
        print("player")
        return self.strategy.buyCards(self, cards, players, cardPile)

    def buyCard(self, card, players, cardPile, payment):
        self.addCard(card, players, cardPile)
        self.removeResources(payment)

    def isPayable(self, hut):
        return self.strategy.isPayable(hut, self.resources)

    def addCard(self, card, players, cardPile):
        self.cards.append(card)
        card.execute(players, cardPile)
        
    def getSymbolCardLists(self):
        result = {}
        for card in [c for c in self.cards if isinstance(c, SymbolCard)]:
            if not card.getSymbol().name in result.keys():
                result[card.getSymbol().name] = []
            result[card.getSymbol().name].append(card)
        return result
   
    def getMultiplierCardsBySymbol(self):
        return groupby(sorted([c for c in self.cards if isinstance(c, MultiplierCard)]), lambda c : c.getSymbol())
    

    def symbolCardPoints(self):
        symbolCardLists = self.getSymbolCardLists()
        points1 = pow(len(symbolCardLists.keys()), 2)
        points2 = pow(len([lst for lst in symbolCardLists.values() if len(lst) == 2]), 2)
        return points1 + points2


    def multiplierCardPoints(self):
        multiplierPoints = 0
        for symbol, cards in self.getMultiplierCardsBySymbol():
            factor = sum([c.getMultiplier() for c in cards])
            if symbol == CardMultiplier.hutcount:
                multiplierPoints += factor * len(self.huts)
            elif symbol == CardMultiplier.foodtrack:
                multiplierPoints += factor * self.foodtrack
            elif symbol == CardMultiplier.toolsum:
                multiplierPoints += factor * sum(self.toolbox.getTools())
            elif symbol == CardMultiplier.personcount:
                multiplierPoints += factor * self.person
        return multiplierPoints

    def getCardScore(self):
        return self.symbolCardPoints() + self.multiplierCardPoints()
       
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
        symbolstr = ", ".join(["%s" %  k for k in sorted(self.getSymbolCardLists().keys())])
        secondCollection = ["%s" % k for k, l in sorted(self.getSymbolCardLists().items()) if len(l) > 1]
        if secondCollection:
            symbolstr += " || " + ", ".join(secondCollection)  
        multistrs = []
        for symbol, cards in self.getMultiplierCardsBySymbol():
            factor = sum([c.getMultiplier() for c in cards])
            multistrs.append("%d x %s" % (factor, symbol.name))
        return """%s%s%s
People: %d, Foodtrack: %d, Food: %d, Tools: %s, One-time tools: %s
Resources: %s
Hutcount: %d
Symbolcards: %s (%d)
Multipliercards: %s (%d)   
score (cardscore): %d (%d)\n""" % (self.colorOS, self.color.name, self.colorOSnormal, \
                  self.getPersonCount(), self.getFoodTrack(), self.resources.count(Resource.food), self.toolbox, self.oneTimeTools,  
                  Resource.coloredOutput(sorted(self.getNonFood())), 
                  len(self.huts), \
                  symbolstr, self.symbolCardPoints(), \
                  ", ".join(multistrs), self.multiplierCardPoints(),\
                  self.getScore(), self.getCardScore())

