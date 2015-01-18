#! /usr/bin/env python3

from Hut import SimpleHut, AnyHut, CountHut
from random import shuffle
from ResourceField import HuntingGrounds, Forest, ClayPit, Quarry, River, Farm,\
    BreedingHut, ToolSmith
from Card import Card, MultiplierCard, SymbolCard, CardAction, CardMultiplier, CardSymbol
from Resource import Resource

class PlacementError(Exception):
    """Exception class for illegal placements"""
    def __init__(self, msg):
        Exception.__init__(self, msg)

class Board:
    """Class representing the gameboard """

    def __init__(self, huts=None):
        self.huntingGrounds = HuntingGrounds()
        self.forest = Forest()
        self.clayPit = ClayPit()
        self.quarry = Quarry()
        self.river = River()
        self.farm = Farm()
        self.breedingHut = BreedingHut()
        self.toolSmith = ToolSmith()
        self.grounds = [self.huntingGrounds, self.forest, self.clayPit, self.quarry, self.river, self.toolSmith, self.farm, self.breedingHut]
        
        if not huts:
            huts = self._defaultHuts()
        
        shuffle(huts)
        div, mod = divmod(len(huts), 4)
        end1 =        div + int(mod > 0)
        end2 = end1 + div + int(mod > 1)
        end3 = end2 + div + int(mod > 2)
        
        self.hutStacks = [huts[0   :end1],
                          huts[end1:end2],
                          huts[end2:end3],
                          huts[end3:    ]]
        
        self.cardPile = [SymbolCard(CardSymbol.weaving, CardAction.food, 3), 
                         SymbolCard(CardSymbol.weaving, CardAction.food, 1),
                         SymbolCard(CardSymbol.time, CardAction.christmas, 0), 
                         SymbolCard(CardSymbol.time, CardAction.farmer, 1),
                         SymbolCard(CardSymbol.healing, CardAction.food, 5), 
                         SymbolCard(CardSymbol.healing, CardAction.joker, 2),
                         SymbolCard(CardSymbol.art, CardAction.tool, 1), 
                         SymbolCard(CardSymbol.art, CardAction.roll, 6),
                         SymbolCard(CardSymbol.pottery, CardAction.food, 7), 
                         SymbolCard(CardSymbol.pottery, CardAction.christmas, 0), 
                         SymbolCard(CardSymbol.transport, CardAction.stone, 2), 
                         SymbolCard(CardSymbol.transport, CardAction.christmas, 0),
                         SymbolCard(CardSymbol.music, CardAction.score, 3), 
                         SymbolCard(CardSymbol.music, CardAction.score, 3),
                         SymbolCard(CardSymbol.writing, CardAction.extracard, 1), 
                         SymbolCard(CardSymbol.writing, CardAction.christmas, 0),
                         MultiplierCard(CardMultiplier.hutBuilder, 1, CardAction.christmas, 0),
                         MultiplierCard(CardMultiplier.hutBuilder, 1, CardAction.food, 4),
                         MultiplierCard(CardMultiplier.hutBuilder, 2, CardAction.christmas, 0),
                         MultiplierCard(CardMultiplier.hutBuilder, 2, CardAction.food, 2),
                         MultiplierCard(CardMultiplier.hutBuilder, 3, CardAction.score, 3),
                         MultiplierCard(CardMultiplier.farmer, 1, CardAction.christmas, 0),
                         MultiplierCard(CardMultiplier.farmer, 1, CardAction.farmer, 1),
                         MultiplierCard(CardMultiplier.farmer, 1, CardAction.stone, 1),
                         MultiplierCard(CardMultiplier.farmer, 2, CardAction.food, 3),
                         MultiplierCard(CardMultiplier.farmer, 2, CardAction.christmas, 0),
                         MultiplierCard(CardMultiplier.toolMaker, 2, CardAction.christmas, 0),
                         MultiplierCard(CardMultiplier.toolMaker, 2, CardAction.christmas, 0),   
                         MultiplierCard(CardMultiplier.toolMaker, 1, CardAction.oneTimeTool, 3),
                         MultiplierCard(CardMultiplier.toolMaker, 1, CardAction.oneTimeTool, 4),
                         MultiplierCard(CardMultiplier.toolMaker, 2, CardAction.oneTimeTool, 2),
                         MultiplierCard(CardMultiplier.shaman, 1, CardAction.stone, 1),
                         MultiplierCard(CardMultiplier.shaman, 1, CardAction.gold, 1),
                         MultiplierCard(CardMultiplier.shaman, 2, CardAction.clay, 1),                                                                                      
                         MultiplierCard(CardMultiplier.shaman, 2, CardAction.roll, 3),
                         MultiplierCard(CardMultiplier.shaman, 1, CardAction.roll, 5),
                         ]
        shuffle(self.cardPile)

    def _defaultHuts(self):
        return [SimpleHut(Resource.wood, Resource.wood, Resource.clay),
                SimpleHut(Resource.wood, Resource.wood, Resource.stone),
                SimpleHut(Resource.wood, Resource.wood, Resource.gold),
                SimpleHut(Resource.wood, Resource.clay, Resource.stone),
                SimpleHut(Resource.wood, Resource.clay, Resource.clay),
                SimpleHut(Resource.wood, Resource.stone, Resource.stone),
                SimpleHut(Resource.wood, Resource.clay, Resource.gold),
                SimpleHut(Resource.wood, Resource.clay, Resource.gold),
                SimpleHut(Resource.wood, Resource.clay, Resource.stone),
                SimpleHut(Resource.wood, Resource.stone, Resource.gold),
                SimpleHut(Resource.wood, Resource.stone, Resource.gold),
                SimpleHut(Resource.clay, Resource.clay, Resource.stone),
                SimpleHut(Resource.clay, Resource.clay, Resource.gold),
                SimpleHut(Resource.clay, Resource.stone, Resource.stone),
                SimpleHut(Resource.clay, Resource.stone, Resource.gold),
                SimpleHut(Resource.clay, Resource.stone, Resource.gold),
                SimpleHut(Resource.stone, Resource.stone, Resource.gold),
                AnyHut(),
                AnyHut(),
                AnyHut(),
                CountHut(4,1),
                CountHut(4,2),
                CountHut(4,3),
                CountHut(4,4),
                CountHut(5,1),
                CountHut(5,2),
                CountHut(5,3),
                CountHut(5,4),
                ]

    def numberOfHutsLeft(self):
        return [len(stack) for stack in self.hutStacks]

    def upperHuts(self):
        return [stack[-1] for stack in self.hutStacks if len(stack) > 0]
    
    def availableHuts(self):
        return [hut for hut in self.upperHuts() if not hut.isOccupied()]
    
    def addHunters(self, count, player):
        self.huntingGrounds.addPerson(count, player)
    
    def addLumberjacks(self, count, player):
        self.forest.addPerson(count, player)
        
    def freeForestSlots(self):
        return self.forest.freeSlots()
    
    def addClayDiggers(self, count, player):
        self.clayPit.addPerson(count, player)
        
    def freeClayPitSlots(self):
        return self.clayPit.freeSlots()
    
    def addStoneDiggers(self, count, player):
        self.quarry.addPerson(count, player)
        
    def freeQuarrySlots(self):
        return self.quarry.freeSlots()

    def addGoldDiggers(self, count, player):
        self.river.addPerson(count, player)
        
    def freeRiverSlots(self):
        return self.river.freeSlots()
 
    def placeOnFarm(self, player):
        self.farm.addPerson(player)
 
    def farmOccupied(self):
        return self.farm.freeSlots() == 0
    
    def placeOnBreedingHut(self, player):
        self.breedingHut.addPerson(player)
        
    def breedingHutOccupied(self):
        return self.breedingHut.freeSlots() == 0
        
    def placeOnToolSmith(self, player):
        self.toolSmith.addPerson(player)
 
    def toolSmithOccupied(self):
        return self.toolSmith.freeSlots() == 0

    def personsOnHuts(self, player):
        return [stack[-1].isOccupiedBy() for stack in self.hutStacks].count(player)

    def personsOnGrounds(self, player):
        return sum([ground.count(player) for ground in self.grounds])

    def person(self, player):
        return self.personsOnGrounds(player) + self.personsOnHuts(player)
    
    def resourceGrounds(self):
        return self.grounds[:-3]
    
    def villageGrounds(self):
        return self.grounds[-3:]
    
    def occupiedCards(self, player):
        return []
    
    def numberOfCardsLeft(self):
        return len(self.cardPile)
    
    def reapResources(self, players):
        player = players[0]
        reapedResources = []
        for ground in self.villageGrounds():
            player.addResources(ground.reapResources(player))

        for card in self.occupiedCards(player):
            player.addCard(players)

#       get occupied grounds
        occupiedGrounds = {} 
        for ground in self.resourceGrounds():
            if ground.count(player):
                occupiedGrounds[ground.abreviation] = ground
        while len(occupiedGrounds):
            resourceAbr = player.chooseReapingResource("".join(occupiedGrounds.keys()))
            player.addResources(occupiedGrounds.pop(resourceAbr).reapResources(player))
                   
        occupiedHuts = [stack[-1] for stack in self.hutStacks if len(stack) > 0 and stack[-1].isOccupiedBy() == player]
        
        for hut in occupiedHuts:
            hut.removePerson()
        return occupiedHuts
    
    
    def popHuts(self, huts):
        for hut in huts:
            [stack.pop() for stack in self.hutStacks if len(stack) > 0 and stack[-1] == hut]
        
    def placeOnHutIndex(self, stackIndex, color):
        self.upperHuts()[stackIndex].placePerson(color)

    def placeOnHut(self, hut, color):
        hut.placePerson(color)
        
    def isFinished(self):
        return [len(stack) for stack in self.hutStacks].count(0) > 0
    
    def hutStacksString(self):
        stackstrings = ["%s" % ("|" * (len(stack)-1) + (str(stack[-1])))  for stack in self.hutStacks if len(stack) > 0]
        hutstacks = ["%d: %-25s" % (idx + 1, s) for idx, s in enumerate(stackstrings)]
        return "%s\n%s" % ("  ".join(hutstacks[:2]), "  ".join(hutstacks[2:])) 
    
    def __str__(self):
        return "Hut Stacks: \n%s" % self.hutStacksString() + "\n" +\
             "\n".join(str(ground) for ground in self.grounds) + "\n"

def main():
    pass

if __name__ == '__main__':
    main()
