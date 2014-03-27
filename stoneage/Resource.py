#! /usr/bin/env python3

from random import randint

class Resource():
    """Base Class to represent a resource field on the board. """
    
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
        toolValueToAdd = player.toolsToUse(self.resourceValue, eyes)
        if toolValueToAdd:
            print("player: " + player.getAbr() + " uses toolvalue: " + str(toolValueToAdd))
        eyesAndTools = eyes + toolValueToAdd
        count = int(eyesAndTools/self.resourceValue)
        return [self.resourceValue for resource in range(count)]

    def __str__(self):
        suffix = ("%-19s: " % self.name)
        filled = [player.getOutputAbr() for player in self.persons for n in range(self.count(player))]
        unfilled = (self.maxPersons - len(filled)) * ["0"]
        return suffix + " ".join(filled + unfilled)
        
class HuntingGrounds(Resource):
    """Class to represent a food resource field on the board."""

    def __init__(self):
        Resource.__init__(self)
        self.resourceValue = 2
        self.name = "Hunting grounds (f)"
        self.abreviation = 'f'

    def freeSlots(self):
        # always room for max person count more people         
        return 10

    def __str__(self):
        filled = [player.getOutputAbr() for player in self.persons for n in range(self.count(player))]
        return self.name + ": " +  " ".join(filled)

class Forest(Resource):
    """Class to represent a wood resource field on the board."""

    def __init__(self):
        Resource.__init__(self)
        self.resourceValue = 3
        self.name = "Forest (w)"
        self.abreviation = 'w'

class ClayPit(Resource):
    """Class to represent a clay resource field on the board."""

    def __init__(self):
        Resource.__init__(self)        
        self.resourceValue = 4
        self.name = "Clay pit (c)"
        self.abreviation = 'c'
        
class Quarry(Resource):
    """Class to represent a stone resource field on the board."""

    def __init__(self):
        Resource.__init__(self)
        self.resourceValue = 5
        self.name = "Quarry (s)"
        self.abreviation = 's'

class River(Resource):
    """Class to represent a gold resource field on the board."""

    def __init__(self):
        Resource.__init__(self)        
        self.resourceValue = 6
        self.name = "River (g)"
        self.abreviation = 'g'
        
class ToolSmith(Resource):
    """Class to represent the tool-smith in the village part of the board"""
    def __init__(self):
        Resource.__init__(self)        
        self.name = "Toolsmith (t)"
        self.abreviation = 't'
        self.resourceValue = 7
        self.maxPersons = 1
        
    def addPerson(self, abr):
        Resource.addPerson(self, 1, abr)
        
    def reapResources(self, player):
        if self.persons.pop(player, None):
            return [7]
        return []
    
class Farm(Resource):
    """Class to represent the farm in the village part of the board"""
    
    def __init__(self):
        Resource.__init__(self)        
        self.name = "Farm (a)"
        self.abreviation = 'a'
        self.resourceValue = 8
        self.maxPersons = 1
        
    def addPerson(self, player):
        Resource.addPerson(self, 1, player)
        
    def reapResources(self, player):
        if self.persons.pop(player, None):
            return [8]
        return []

class BreedingHut(Resource):
    """Class to represent the breeding hut in the village part of the board"""
    
    def __init__(self):
        Resource.__init__(self)        
        self.name = "Breeding hut (b)"
        self.abreviation = 'b'
        self.maxPersons = 2
        
    def addPerson(self, player):
        Resource.addPerson(self, 2, player)
        
    def reapResources(self, player):
        if self.persons.pop(player, None):
            return [9]
        return []


if __name__ == '__main__':
    print("hallo")
          
