#! /usr/bin/env python3

from random import randint

class Resource():
    """Class to represent a resource field on the board. """
    
    def __init__(self):
        self.maxPersons = 7
        self.persons = ""

    def addPerson(self, n, playerAbr):
        if n == 0: return
        if (self.persons.count(playerAbr) > 0):
            from Board import PlacementError
            raise PlacementError("Player %s already added person to the %s" % (playerAbr, self.name))
        if (len(self.persons) + n > self.maxPersons):
            from Board import PlacementError
            raise PlacementError("Not room for %d further persons in the %s" % (n, self.name))
        self.persons += n * playerAbr
    
    def count(self, playerAbr):
        return self.persons.count(playerAbr)
    
    def freeSlots(self):
        return self.maxPersons - len(self.persons)

    def reapResources(self, playerAbr):
        count = int(sum([randint(1, 6) for dice in range(0, self.count(playerAbr))])/self.resourceValue)
        self.persons = "".join([ch for ch in self.persons if ch != playerAbr])
        return [self.resourceValue for resource in  range(0, count)]

    def toString(self):
        return ("%-19s" % self.name) + ": " + " ".join(ch for ch in self.persons + "O" * (self.maxPersons - len(self.persons)))
        
class HuntingGrounds(Resource):
    """Class to represent a food resource field on the board."""

    def __init__(self):
        Resource.__init__(self)
        self.resourceValue = 2
        self.name = "Hunting grounds (f)"

    def freeSlots(self):
        return 10

    def toString(self):
        return self.name + ": " + " ".join([ch for ch in self.persons])


class Forest(Resource):
    """Class to represent a wood resource field on the board."""

    def __init__(self):
        Resource.__init__(self)
        self.resourceValue = 3
        self.name = "Forest (w)"

class ClayPit(Resource):
    """Class to represent a clay resource field on the board."""

    def __init__(self):
        Resource.__init__(self)        
        self.resourceValue = 4
        self.name = "Clay pit (c)"
        
class Quarry(Resource):
    """Class to represent a stone resource field on the board."""

    def __init__(self):
        Resource.__init__(self)
        self.resourceValue = 5
        self.name = "Quarry (s)"

class River(Resource):
    """Class to represent a gold resource field on the board."""

    def __init__(self):
        Resource.__init__(self)        
        self.resourceValue = 6
        self.name = "River (g)"
    
class Farm(Resource):
    """Class to represent the farm in the village part of the board"""
    
    def __init__(self):
        Resource.__init__(self)        
        self.name = "Farm (a)"
        self.resourceValue = 7
        self.maxPersons = 1
        
    def addPerson(self, abr):
        Resource.addPerson(self, 1, abr)
        
    def reapResources(self, playerAbr):
        if playerAbr == self.persons:
            self.persons = ""
            return [7]
        return []

class BreedingHut(Resource):
    """Class to represent the breeding hut in the village part of the board"""
    
    def __init__(self):
        Resource.__init__(self)        
        self.name = "Breeding hut (b)"
        self.maxPersons = 2
        
    def addPerson(self, abr):
        Resource.addPerson(self, 2, abr)
        
    def reapResources(self, playerAbr):
        if self.persons and playerAbr == self.persons[0]:
            self.persons = ""
            return [8]
        return []

class ToolSmith(Resource):
    """Class to represent the tool-smith in the village part of the board"""
    def __init__(self):
        Resource.__init__(self)        
        self.name = "Toolsmith (t)"
        self.resourceValue = 9
        self.maxPersons = 1
        
    def addPerson(self, abr):
        Resource.addPerson(self, 1, abr)
        
    def reapResources(self, playerAbr):
        if playerAbr == self.persons:
            self.persons = ""
            return [9]
        return []

if __name__ == '__main__':
    print("hallo")
          
