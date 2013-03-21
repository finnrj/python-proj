#! /usr/bin/env python3

from Hut import SimpleHut, AnyHut, CountHut
from random import shuffle
from Resource import HuntingGrounds, Forest, ClayPit, Quarry, River

from math import floor

class Board:
    """Class representing the gameboard """

    players = []
    
    def __init__(self, huts=None):
        self.huntingGrounds = HuntingGrounds()
        self.forest = Forest()
        self.clayPit = ClayPit()
        self.quarry = Quarry()
        self.river = River()
        self.grounds = [self.huntingGrounds, self.forest, self.clayPit, self.quarry, self.river]
        
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

    def availableHuts(self):
        return [stack[-1] for stack in self.hutStacks if len(stack) > 0 and not stack[-1].isOccupied()]

    def addHunters(self, count, abr):
        self.huntingGrounds.addPerson(count, abr)
    
    def addLumberjacks(self, count, abr):
        self.forest.addPerson(count, abr)
        
    def freeForestSlots(self):
        return self.forest.freeSlots()
    
    def addClayDiggers(self, count, abr):
        self.clayPit.addPerson(count, abr)
        
    def freeClayPitSlots(self):
        return self.clayPit.freeSlots()
    
    def addStoneDiggers(self, count, abr):
        self.quarry.addPerson(count, abr)
        
    def freeQuarrySlots(self):
        return self.quarry.freeSlots()

    def addGoldDiggers(self, count, abr):
        self.river.addPerson(count, abr)
        
    def freeRiverSlots(self):
        return self.river.freeSlots()
        
    def personsOnHuts(self, abr):
        return [stack[-1].isOccupiedBy() for stack in self.hutStacks].count(abr)

    def personsOnGrounds(self, abr):
        return sum([ground.count(abr) for ground in self.grounds])

    def personCount(self, abr):
        return self.personsOnGrounds(abr) + self.personsOnHuts(abr)
    
    def reapResources(self, abr):
        reapedResources = []
        for ground in self.grounds:
            reapedResources.extend(ground.reapResources(abr))
        
        occupiedHuts = [stack[-1] for stack in self.hutStacks if len(stack) > 0 and stack[-1].isOccupiedBy() == abr]
        
        for hut in occupiedHuts:
            hut.removePerson()
        return (reapedResources, occupiedHuts)
    
    def popHuts(self, huts):
        for hut in huts:
            [stack.pop() for stack in self.hutStacks if len(stack) > 0 and stack[-1] == hut]
        
    def placeOnHut(self, hut, color):
        hut.placePerson(color)
        
    def isFinished(self):
        return [len(stack) for stack in self.hutStacks].count(0) > 0
    
    def toString(self):
        stackstrings = ["[" * (len(stack)-1) + stack[-1].toString() for stack in self.hutStacks if len(stack) > 0]
        return "Hut Stacks:\n%s" % "  ".join(stackstrings) + "\n" +\
             "\n".join(ground.toString() for ground in self.grounds)

def main():
    pass

if __name__ == '__main__':
    main()
