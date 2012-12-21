#! /usr/bin/env python3

from Hut import Hut
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
        div = floor(len(huts) / 4)
        self.hutStacks = [huts[0:div],
                          huts[div: 2 * div],
                          huts[2 * div: 3 * div],
                          huts[3 * div:]]

    def _defaultHuts(self):
        return [Hut(3, 3, 4),
                Hut(3, 3, 5),
                Hut(3, 3, 6),
                Hut(3, 4, 5),
                Hut(3, 4, 4),
                Hut(3, 5, 5),
                Hut(3, 4, 6),
                Hut(3, 4, 6),
                Hut(3, 4, 5),
                Hut(3, 5, 6),
                Hut(3, 5, 6),
                Hut(4, 4, 5),
                Hut(4, 4, 6),
                Hut(4, 5, 5),
                Hut(4, 5, 6),
                Hut(4, 5, 6),
                Hut(5, 5, 6)]

    def numberOfHutsLeft(self):
        return [len(stack) for stack in self.hutStacks]

    def availableHuts(self):
        return [stack[-1] for stack in self.hutStacks if not stack[-1].isOccupied()]

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
        return sum([resource.count() for resource in self.grounds]) + (4 - len(self.availableHuts()))
    
    def reapResources(self):
        reapedResources = [resource.reapResources() for resource in self.grounds]
        boughtHuts = [stack.pop() for stack in self.hutStacks if stack[-1].isOccupied()]
        for hut in boughtHuts:
            hut.removePerson()
        
    def placeOnHut(self, hut):
        hut.placePerson()

def main():
    pass

if __name__ == '__main__':
    main()
