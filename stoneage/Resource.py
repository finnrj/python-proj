#! /usr/bin/env python3

from random import randint

class Resource():
    """Class to represent a resource field on the board. """

    def __init__(self):
        pass

    def addPerson(self, n):
        self.n = n

    def reapResources(self):
        count = int(sum([randint(1, 6) for roll in range(0, self.n)])/self.resourceValue)
        return [self.newResource() for resource in  range(0, count)]

class HuntingGrounds(Resource):
    """Class to represent a food resource field on the board."""

    def __init__(self):
        self.resourceValue = 2

    def newResource(self):
        return Food()

class Food:
    pass

class Forest(Resource):
    """Class to represent a wood resource field on the board."""

    def __init__(self):
        self.resourceValue = 3

    def newResource(self):
        return Wood()

class Wood:
    pass

class ClayPit(Resource):
    """Class to represent a clay resource field on the board."""

    def __init__(self):
        self.resourceValue = 4

    def newResource(self):
        return Brick()

class Brick:
    pass

class Quarry(Resource):
    """Class to represent a stone resource field on the board."""

    def __init__(self):
        self.resourceValue = 5

    def newResource(self):
        return Stone()

class Stone:
    pass

class River(Resource):
    """Class to represent a gold resource field on the board."""

    def __init__(self):
        self.resourceValue = 6

    def newResource(self):
        return Gold()

class Gold:
    pass
    
if __name__ == '__main__':
    print("hallo")
          
