#! /usr/bin/env python3

from Hut import SimpleHut, AnyHut, CountHut
from random import shuffle
from Resource import HuntingGrounds, Forest, ClayPit, Quarry, River, Farm,\
    BreedingHut, ToolSmith
from Card import Card, MultiplierCard, SymbolCard

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
        
        self.cardPile = [SymbolCard("weaving", "food", 3), SymbolCard("weaving", "food", 1),
                         SymbolCard("time", "christmas", 0), SymbolCard("time", "foodTrack", 1),
                         SymbolCard("healing", "food", 5), SymbolCard("healing", "joker", 2),
                         SymbolCard("art", "tool", 1), SymbolCard("art", "roll", 6),
                         SymbolCard("pottery", "food", 7), SymbolCard("pottery", "christmas", 0), 
                         SymbolCard("transport", "stone", 2), SymbolCard("transport", "christmas", 0),
                         SymbolCard("music", "score", 3), SymbolCard("music", "score", 3),
                         SymbolCard("writing", "extraCard", 1), SymbolCard("writing", "christmas", 0),
                         MultiplierCard("hutBuilder", 1, "christmas", 0),
                         MultiplierCard("hutBuilder", 1, "food", 4),
                         MultiplierCard("hutBuilder", 2, "christmas", 0),
                         MultiplierCard("hutBuilder", 2, "food", 2),
                         MultiplierCard("hutBuilder", 3, "score", 3),
                         MultiplierCard("farmer", 1, "christmas", 0),
                         MultiplierCard("farmer", 1, "foodTrack", 1),
                         MultiplierCard("farmer", 1, "stone", 1),
                         MultiplierCard("farmer", 2, "food", 3),
                         MultiplierCard("farmer", 2, "christmas", 0),
                         MultiplierCard("toolMaker", 2, "christmas", 0),
                         MultiplierCard("toolMaker", 2, "christmas", 0),   
                         MultiplierCard("toolMaker", 1, "oneTimeTool", 3),
                         MultiplierCard("toolMaker", 1, "oneTimeTool", 4),
                         MultiplierCard("toolMaker", 2, "oneTimeTool", 2),
                         MultiplierCard("shaman", 1, "stone", 1),
                         MultiplierCard("shaman", 1, "gold", 1),
                         MultiplierCard("shaman", 2, "clay", 1),                                                                                      
                         MultiplierCard("shaman", 2, "roll", 3),
                         MultiplierCard("shaman", 1, "roll", 5),
                         ]
        shuffle(self.cardPile)

    def _defaultHuts(self):
        return [SimpleHut(3, 3, 4),
                SimpleHut(3, 3, 5),
                SimpleHut(3, 3, 6),
                SimpleHut(3, 4, 5),
                SimpleHut(3, 4, 4),
                SimpleHut(3, 5, 5),
                SimpleHut(3, 4, 6),
                SimpleHut(3, 4, 6),
                SimpleHut(3, 4, 5),
                SimpleHut(3, 5, 6),
                SimpleHut(3, 5, 6),
                SimpleHut(4, 4, 5),
                SimpleHut(4, 4, 6),
                SimpleHut(4, 5, 5),
                SimpleHut(4, 5, 6),
                SimpleHut(4, 5, 6),
                SimpleHut(5, 5, 6),
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
    
    def addHunters(self, count, playerAbr):
        self.huntingGrounds.addPerson(count, playerAbr)
    
    def addLumberjacks(self, count, playerAbr):
        self.forest.addPerson(count, playerAbr)
        
    def freeForestSlots(self):
        return self.forest.freeSlots()
    
    def addClayDiggers(self, count, playerAbr):
        self.clayPit.addPerson(count, playerAbr)
        
    def freeClayPitSlots(self):
        return self.clayPit.freeSlots()
    
    def addStoneDiggers(self, count, playerAbr):
        self.quarry.addPerson(count, playerAbr)
        
    def freeQuarrySlots(self):
        return self.quarry.freeSlots()

    def addGoldDiggers(self, count, playerAbr):
        self.river.addPerson(count, playerAbr)
        
    def freeRiverSlots(self):
        return self.river.freeSlots()
 
    def placeOnFarm(self, player):
        self.farm.addPerson(player)
 
    def farmOccupied(self):
        return self.farm.freeSlots() == 0
    
    def placeOnBreedingHut(self, playerAbr):
        self.breedingHut.addPerson(playerAbr)
        
    def breedingHutOccupied(self):
        return self.breedingHut.freeSlots() == 0
        
    def placeOnToolSmith(self, playerAbr):
        self.toolSmith.addPerson(playerAbr)
 
    def toolSmithOccupied(self):
        return self.toolSmith.freeSlots() == 0

    def personsOnHuts(self, player):
        return [stack[-1].isOccupiedBy() for stack in self.hutStacks].count(player.getAbr())

    def personsOnGrounds(self, player):
        return sum([ground.count(player) for ground in self.grounds])

    def personCount(self, player):
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
                   
        occupiedHuts = [stack[-1] for stack in self.hutStacks if len(stack) > 0 and stack[-1].isOccupiedBy() == player.getAbr()]
        
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
    
    def __str__(self):
        stackstrings = ["[" * (len(stack)-1) + str(stack[-1]) for stack in self.hutStacks if len(stack) > 0]
        return "Hut Stacks:\n%s" % "  ".join(stackstrings) + "\n" +\
             "\n".join(str(ground) for ground in self.grounds) + "\n"

def main():
    pass

if __name__ == '__main__':
    main()
