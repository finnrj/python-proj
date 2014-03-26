#! /usr/bin/env python3

from random import randint

class Resource():
    """Base Class to represent a resource field on the board. """
    
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

    def reapResources(self, player):
        numberOfPersons = self.count(player.getAbr())
        if numberOfPersons == 0:
            return []
        eyes = sum([randint(1, 6) for dice in range(0, numberOfPersons)])
        toolValueToAdd = player.toolsToUse(self.resourceValue, eyes)
        if toolValueToAdd:
            print("player: " + player.getAbr() + " uses toolvalue: " + str(toolValueToAdd))
        eyesAndTools = eyes + toolValueToAdd
        count = int(eyesAndTools/self.resourceValue)
        self.persons = "".join([ch for ch in self.persons if ch != player.getAbr()])
        return [self.resourceValue for resource in  range(0, count)]

    def colorAbreviations(self, groundString):
        groundString = groundString.replace("r","\033[1;31mr\033[0m")
        groundString = groundString.replace("g","\033[32mg\033[0m")
        groundString = groundString.replace("b","\033[1;34mb\033[0m")
        groundString = groundString.replace("y","\033[33my\033[0m")
        return groundString
    
    def __str__(self):        
        return ("%-19s" % self.name) + self.colorAbreviations(": " + " ".join(ch for ch in self.persons + "O" * (self.maxPersons - len(self.persons))))
        
class HuntingGrounds(Resource):
    """Class to represent a food resource field on the board."""

    def __init__(self):
        Resource.__init__(self)
        self.resourceValue = 2
        self.name = "Hunting grounds (f)"
        self.abreviation = 'f'

    def freeSlots(self):
        return 10

    def __str__(self):
        return self.name + ": " + self.colorAbreviations(" ".join([ch for ch in self.persons]))


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
        if player.getAbr() == self.persons:
            self.persons = ""
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
        
    def addPerson(self, abr):
        Resource.addPerson(self, 1, abr)
        
    def reapResources(self, player):
        if player.getAbr() == self.persons:
            self.persons = ""
            return [8]
        return []

class BreedingHut(Resource):
    """Class to represent the breeding hut in the village part of the board"""
    
    def __init__(self):
        Resource.__init__(self)        
        self.name = "Breeding hut (b)"
        self.abreviation = 'b'
        self.maxPersons = 2
        
    def addPerson(self, abr):
        Resource.addPerson(self, 2, abr)
        
    def reapResources(self, player):
        if self.persons and player.getAbr() == self.persons[0]:
            self.persons = ""
            return [9]
        return []


if __name__ == '__main__':
    print("hallo")
          
