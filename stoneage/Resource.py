#! /usr/bin/env python3

from random import randint

class Resource():
    types = {"food" : 2,
            "wood" : 3,
             "clay" : 4,
             "stone" : 5,
             "gold" : 6}

    def __init__(self, resourceType):
        self.type = Resource.types[resourceType]

    def addPerson(self, n):
        self.n = n

    def getResources(self):
        return int(sum([randint(1,6) for roll in range(0, self.n)])/self.type)
    
if __name__ == '__main__':
    print("hallo")
          
