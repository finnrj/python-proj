#! /usr/bin/env python3
from itertools import permutations

class Hut:
    """Super Class representing a 'hut' building tile"""
    
    def __init__(self):
        self.player = ""

    def placePerson(self, color):
        self.player = color

    def removePerson(self):
        self.player = ""

    def isOccupied(self):
        return (self.player != "")

    def isOccupiedBy(self):
        return self.player
    
    def value(self):
        return sum(self._costs)
    
    def containsOnlyFood(self, resources):
        return sum([resources.count(num) for num in [3, 4, 5, 6]]) == 0
    
    def toString(self):
        return self.hutAsString() + self.player
    
class SimpleHut(Hut):
    """ hut with exactly three resources """
    def __init__(self, r1, r2, r3):
        Hut.__init__(self)
        self._costs = [r1, r2, r3]

    # used in player.adjustResources
    # sets self._costs / returns costs
    def costs(self, resources):
        return self._costs

    def missing(self, resources):
        clone = resources[:]
        missing = []
        for res in self._costs:
            try:
                clone.remove(res)
            except:
                missing.append(res)
        return missing
    
    def hutAsString(self):
        return str(self._costs)
    
class AnyHut(Hut):
    """ 1-7 Hut """
    def __init__(self):
        Hut.__init__(self)
        self._costs = []

    def costs(self, resources):
        nonFood = [resource for resource in resources if resource != 2]
        self._costs = nonFood[:7]
        return nonFood[:7]
        
    def missing(self, resources):
        if len(resources) == 0 or self.containsOnlyFood(resources) :
            return [3]
        return [] 
    
    def hutAsString(self):
        return "[Any]"
    
class CountHut(Hut):
    """ Hut with four or five resources of 1 to 5 different types"""
    def __init__(self, resourceCount, typesCount):
        Hut.__init__(self)
        self.resourceCount = resourceCount
        self.typesCount = typesCount
        self._costs = []

    def costs(self, resources):
        result = []        
        nonFood = [resource for resource in resources if resource != 2]
        if self.missing (resources):
            return result

        availableTypes = [num for num in [3, 4, 5, 6] if resources.count(num) > 0 ]
        for permutation in permutations(availableTypes, self.typesCount):
            if self.sufficientResources(nonFood, permutation):
                permutationResources = [resource for resource in nonFood if resource in permutation]
                result.extend(permutation)
                for resource in permutation:
                    permutationResources.remove(resource)
                result.extend(permutationResources[:(self.resourceCount - self.typesCount)])
                self._costs = result
                return result
        raise("CountHut:missing is probably false")

    def sufficientResources(self, nonFood, p):
        return sum([nonFood.count(num) for num in p if nonFood.count(num) > 0]) >= self.resourceCount

    def tooFewDifferentTypes(self, typesCounts):
        return typesCounts.count(0) > 4 - self.typesCount

    def tooFewResources(self, resources):
        availableTypes = [num for num in [3, 4, 5, 6] if resources.count(num) > 0 ]
        for permutation in permutations(availableTypes, self.typesCount):
            if self.sufficientResources(resources, permutation):
                return False
        return True

    def missing(self, resources):
        if len(resources) == 0 or self.containsOnlyFood(resources) :
            necessaryTypes = [3, 4, 5, 6][:self.typesCount] 
            return necessaryTypes + self.allWood(self.resourceCount - self.typesCount)
        
        typesCounts = [resources.count(num) for num in [3, 4, 5, 6]]
        if self.tooFewDifferentTypes(typesCounts):
            result = self.findMissingResourceTypes(typesCounts)
            return result + self.allWood(self.resourceCount - (sum(typesCounts) + len(result)))
          
        if self.tooFewResources(resources):
            availableTypes = [num for num in [3, 4, 5, 6] if resources.count(num) > 0 ]
            firstPossibleTypes = availableTypes[:self.typesCount]
            return (self.resourceCount - sum([resources.count(num) for num in firstPossibleTypes])) * [firstPossibleTypes[0]] 
        return []
    
    def findMissingResourceTypes(self, typesCounts):
        missingTypesCount = typesCounts.count(0) - (4 - self.typesCount)
        result = []
        for idx, count in enumerate(typesCounts):
            if count == 0:
                result.append(idx + 3)
                missingTypesCount -= 1
            if missingTypesCount == 0:
                return result
        raise("findMissingResourceTypes called with illegal typesCounts: %s" % str(typesCounts))
    
    def allWood(self, count):
        return count * [3]
        
    def hutAsString(self):
        return "[Count:%d,%d]" %(self.resourceCount, self.typesCount)


def main():
    pass

if __name__ == '__main__':
    main()
