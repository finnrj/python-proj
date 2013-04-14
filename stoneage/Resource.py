#! /usr/bin/env python3

from random import randint

class Resource():
    """Class to represent a resource field on the board. """

    maxPersons = 7
    
    def __init__(self):
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
        return ("%-19s" % self.name) + ": " + " ".join(ch for ch in self.persons + "O" * (7 - len(self.persons)))
        
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
    

if __name__ == '__main__':
    print("hallo")
          
