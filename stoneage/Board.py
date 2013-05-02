#! /usr/bin/env python3

from Hut import SimpleHut, AnyHut, CountHut
from random import shuffle
from Resource import HuntingGrounds, Forest, ClayPit, Quarry, River, Farm,\
    BreedingHut

class PlacementError(Exception):
    """Exception class for illegal placements"""
    def __init__(self, msg):
        Exception.__init__(self, msg)

class Board:
    """Class representing the gameboard """

    players = []
    
    def __init__(self, huts=None):
        self.huntingGrounds = HuntingGrounds()
        self.forest = Forest()
        self.clayPit = ClayPit()
        self.quarry = Quarry()
        self.river = River()
        self.farm = Farm()
        self.breedingHut = BreedingHut()
        self.grounds = [self.huntingGrounds, self.forest, self.clayPit, self.quarry, self.river, self.farm, self.breedingHut]
        
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
 
    def placeOnFarm(self, playerAbr):
        self.farm.addPerson(playerAbr)
 
    def farmOccupied(self):
        return self.farm.freeSlots() == 0
    
    def placeOnBreedingHut(self, playerAbr):
        self.breedingHut.addPerson(playerAbr)
        
    def breedingHutOccupied(self):
        return self.breedingHut.freeSlots() == 0
        
    def personsOnHuts(self, playerAbr):
        return [stack[-1].isOccupiedBy() for stack in self.hutStacks].count(playerAbr)

    def personsOnGrounds(self, playerAbr):
        return sum([ground.count(playerAbr) for ground in self.grounds])

    def personCount(self, playerAbr):
        return self.personsOnGrounds(playerAbr) + self.personsOnHuts(playerAbr)
    
    def reapResources(self, playerAbr):
        reapedResources = []
        for ground in self.grounds:
            reapedResources.extend(ground.reapResources(playerAbr))
        
        occupiedHuts = [stack[-1] for stack in self.hutStacks if len(stack) > 0 and stack[-1].isOccupiedBy() == playerAbr]
        
        for hut in occupiedHuts:
            hut.removePerson()
        return (reapedResources, occupiedHuts)
    
    def popHuts(self, huts):
        for hut in huts:
            [stack.pop() for stack in self.hutStacks if len(stack) > 0 and stack[-1] == hut]
        
    def placeOnHutIndex(self, stackIndex, color):
        self.upperHuts()[stackIndex].placePerson(color)

    def placeOnHut(self, hut, color):
        hut.placePerson(color)
        
    def isFinished(self):
        return [len(stack) for stack in self.hutStacks].count(0) > 0
    
    def toString(self):
        stackstrings = ["[" * (len(stack)-1) + stack[-1].toString() for stack in self.hutStacks if len(stack) > 0]
        return "Hut Stacks:\n%s" % "  ".join(stackstrings) + "\n" +\
             "\n".join(ground.toString() for ground in self.grounds) + "\n"

def main():
    pass

if __name__ == '__main__':
    main()
