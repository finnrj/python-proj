#! /usr/bin/env python3

from random import randint
from Resource import Resource

class ResourceField():
    """Base Class to represent a Resource field on the board. """
    
    def __init__(self):
        self.maxPersons = 7
        self.persons = {}

    def addPerson(self, n, player):
        if n == 0: return
        if (player in self.persons):
            from Board import PlacementError
            raise PlacementError("Player %s already added person to the %s" % (player.getColor(),
                                                                                self.name))
        if (sum(self.persons.values()) + n > self.maxPersons):
            from Board import PlacementError
            raise PlacementError("Not room for %d further persons in the %s" % (n, self.name))
        self.persons[player] = n
    
    def count(self, player):
        return self.persons.get(player, 0)
    
    def freeSlots(self):
        return self.maxPersons - sum(self.persons.values())

    def reapResources(self, player):
        numberOfPersons = self.persons.pop(player, 0)
        if numberOfPersons == 0:
            return []
        eyes = sum([randint(1, 6) for dice in range(0, numberOfPersons)])
        toolValueToAdd = player.toolsToUse(self.resource, eyes)
        if toolValueToAdd:
            print("player: " + player.getAbr() + " uses toolvalue: " + str(toolValueToAdd))
        eyesAndTools = eyes + toolValueToAdd
        count = int(eyesAndTools/self.resource.value)
        return [self.resource for resource in range(count)]

    def __str__(self):
        suffix = ("%-19s: " % self.name)
        filled = [player.getOutputAbr() for player in self.persons for n in range(self.count(player))]
        unfilled = (self.maxPersons - len(filled)) * ["0"]
        return suffix + " ".join(filled + unfilled)
        
class HuntingGrounds(ResourceField):
    """Class to represent a food Resource field on the board."""

    def __init__(self):
        ResourceField.__init__(self)
        self.resource = Resource.food
        self.name = "Hunting grounds (f)"
        self.abreviation = 'f'

    def freeSlots(self):
        # always room for max person count more people         
        return 10

    def __str__(self):
        filled = [player.getOutputAbr() for player in self.persons for n in range(self.count(player))]
        return self.name + ": " +  " ".join(filled)

class Forest(ResourceField):
    """Class to represent a wood Resource field on the board."""

    def __init__(self):
        ResourceField.__init__(self)
        self.resource = Resource.wood
        self.name = "Forest (w)"
        self.abreviation = 'w'

class ClayPit(ResourceField):
    """Class to represent a clay Resource field on the board."""

    def __init__(self):
        ResourceField.__init__(self)        
        self.resource = Resource.clay
        self.name = "Clay pit (p)"
        self.abreviation = 'p'
        
class Quarry(ResourceField):
    """Class to represent a stone Resource field on the board."""

    def __init__(self):
        ResourceField.__init__(self)
        self.resource = Resource.stone
        self.name = "Quarry (s)"
        self.abreviation = 's'

class River(ResourceField):
    """Class to represent a gold Resource field on the board."""

    def __init__(self):
        ResourceField.__init__(self)        
        self.resource = Resource.gold
        self.name = "River (g)"
        self.abreviation = 'g'
        
class ToolSmith(ResourceField):
    """Class to represent the tool-smith in the village part of the board"""
    def __init__(self):
        ResourceField.__init__(self)        
        self.name = "Toolsmith (t)"
        self.abreviation = 't'
        self.resource = Resource.tool
        self.maxPersons = 1
        
    def addPerson(self, abr):
        ResourceField.addPerson(self, 1, abr)
        
    def reapResources(self, player):
        if self.persons.pop(player, None):
            return [self.resource]
        return []
    
class Farm(ResourceField):
    """Class to represent the farm in the village part of the board"""
    
    def __init__(self):
        ResourceField.__init__(self)        
        self.name = "Farm (a)"
        self.abreviation = 'a'
        self.resource = Resource.foodtrack
        self.maxPersons = 1
        
    def addPerson(self, player):
        ResourceField.addPerson(self, 1, player)
        
    def reapResources(self, player):
        if self.persons.pop(player, None):
            return [self.resource]
        return []

class BreedingHut(ResourceField):
    """Class to represent the breeding hut in the village part of the board"""
    
    def __init__(self):
        ResourceField.__init__(self)        
        self.name = "Breeding hut (b)"
        self.abreviation = 'b'
        self.maxPersons = 2
        self.resource = Resource.person
        
    def addPerson(self, player):
        ResourceField.addPerson(self, 2, player)
        
    def reapResources(self, player):
        if self.persons.pop(player, None):
            return [self.resource]
        return []


if __name__ == '__main__':
    print("hallo")
          
