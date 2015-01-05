'''
Created on Jan 4, 2015

@author: finn
'''
from enum import IntEnum

class Resource(IntEnum):
    '''
    classdocs
    '''

    food = 2
    wood = 3
    clay = 4
    stone = 5
    gold = 6
    tool = 7
    farmer = 8
    person = 9
    joker = 10

    
    @classmethod
    def from_value(cls, value):
        for name, resource in Resource.__members__():
            if resource.value == value:
                return resource
        return None
    

        