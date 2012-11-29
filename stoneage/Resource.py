#! /usr/bin/env python3

from random import randint

class PlacementError(Exception):
    """Exception class for illegal placements"""
    def __init__(self, msg):
        Exception.__init__(self, msg)

class Resource():
    """Class to represent a resource field on the board. """

    def __init__(self):
        self.n = 0

    def addPerson(self, n):
        if self.n == 0:
            self.n = n
        else:
            raise PlacementError("Already added person to this Resource")
    
    def count(self):
        return self.n

    def reapResources(self):
        count = int(sum([randint(1, 6) for dice in range(0, self.n)])/self.resourceValue)
        self.n = 0
        return [self.resourceValue for resource in  range(0, count)]

class HuntingGrounds(Resource):
    """Class to represent a food resource field on the board."""

    def __init__(self):
        Resource.__init__(self)
        self.resourceValue = 2

class Forest(Resource):
    """Class to represent a wood resource field on the board."""

    def __init__(self):
        Resource.__init__(self)
        self.resourceValue = 3

class ClayPit(Resource):
    """Class to represent a clay resource field on the board."""

    def __init__(self):
        Resource.__init__(self)        
        self.resourceValue = 4

class Quarry(Resource):
    """Class to represent a stone resource field on the board."""

    def __init__(self):
        Resource.__init__(self)
        self.resourceValue = 5

class River(Resource):
    """Class to represent a gold resource field on the board."""

    def __init__(self):
        Resource.__init__(self)        
        self.resourceValue = 6

if __name__ == '__main__':
    print("hallo")
          
