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

    def addHunters(self, count):
        self.huntingGrounds.addPerson(count)
    
    def addLumberjacks(self, count):
        self.forest.addPerson(count)
    
    def addClayDiggers(self, count):
        self.clayPit.addPerson(count)
    
    def addStoneDiggers(self, count):
        self.quarry.addPerson(count)

    def addGoldDiggers(self, count):
        self.river.addPerson(count)
        
    def personCount(self):
        return sum([ground.count() for ground in self.grounds]) + (4 - len(self.availableHuts()))
    
    def reapResources(self):
        reapedResources = []
        for ground in self.grounds:
            reapedResources.extend(ground.reapResources())
        
        boughtHuts = [stack.pop() for stack in self.hutStacks if stack[-1].isOccupied()]
        for hut in boughtHuts:
            hut.removePerson()
        return (reapedResources, boughtHuts)
        
    def placeOnHut(self, hut):
        hut.placePerson()
        
    def isFinished(self):
        return [len(stack) for stack in self.hutStacks].count(0) > 0

def main():
    pass

if __name__ == '__main__':
    main()
