#! /usr/bin/env python3

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
    foodtrack = 8
    person = 9
    joker = 10

    
    def getColoredName(self):
        outputColors = {Resource.food:  "48;5;10",
                        Resource.wood:  "48;5;130",
                        Resource.clay:  "48;5;173",
                        Resource.stone: "48;5;7",
                        Resource.gold:  "48;5;220",
                        Resource.joker: "48;5;30"}
        return "\033[%sm%s\033[0m" % (outputColors[self], self._name_)
    
    @classmethod
    def coloredOutput(clz,resources):
        return "[%s]" % ",".join([resource.getColoredName() for resource in resources])

    @classmethod
    def getByValue(clz,value):
        for member in clz.__members__.values():
            if member.value == value:
                return member
        return None
            
if __name__ == '__main__':
    for name, resource in Resource.__members__.items():
        print(name, resource, resource.getColoredName())