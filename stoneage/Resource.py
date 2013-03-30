#! /usr/bin/env python3

from random import randint

class PlacementError(Exception):
    """Exception class for illegal placements"""
    def __init__(self, msg):
        Exception.__init__(self, msg)

class Resource():
    """Class to represent a resource field on the board. """

    maxPersons = 7
    
    def __init__(self):
        self.persons = ""

    def addPerson(self, n, abr):
        if n == 0: return
        if (self.persons.count(abr) > 0):
            raise PlacementError("Player %s already added person to the %s" % (abr, self.name))
        if (len(self.persons) + n > self.maxPersons):
            raise PlacementError("Not room for %d further persons in the %s" % (n, self.name))
        self.persons += n * abr
    
    def count(self, abr):
        return self.persons.count(abr)
    
    def freeSlots(self):
        return self.maxPersons - len(self.persons)

    def reapResources(self, abr):
        count = int(sum([randint(1, 6) for dice in range(0, self.count(abr))])/self.resourceValue)
        self.persons = "".join([ch for ch in self.persons if ch != abr])
        return [self.resourceValue for resource in  range(0, count)]

    def toString(self):
        return ("%-15s" % self.name) + ": " + " ".join(ch for ch in self.persons + "O" * (7 - len(self.persons)))
        
class HuntingGrounds(Resource):
    """Class to represent a food resource field on the board."""

    def __init__(self):
        Resource.__init__(self)
        self.resourceValue = 2
        self.name = "Hunting grounds"

    def freeSlots(self):
        return 10

    def toString(self):
        return self.name + ": " + " ".join([ch for ch in self.persons])


class Forest(Resource):
    """Class to represent a wood resource field on the board."""

    def __init__(self):
        Resource.__init__(self)
        self.resourceValue = 3
        self.name = "Forest"

class ClayPit(Resource):
    """Class to represent a clay resource field on the board."""

    def __init__(self):
        Resource.__init__(self)        
        self.resourceValue = 4
        self.name = "Clay pit"
        
class Quarry(Resource):
    """Class to represent a stone resource field on the board."""

    def __init__(self):
        Resource.__init__(self)
        self.resourceValue = 5
        self.name = "Quarry"

class River(Resource):
    """Class to represent a gold resource field on the board."""

    def __init__(self):
        Resource.__init__(self)        
        self.resourceValue = 6
        self.name = "River"

    
    
    

if __name__ == '__main__':
    print("hallo")
          
