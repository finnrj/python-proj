#! /usr/bin/env python3
from itertools import permutations
from Resource import Resource

class Hut:
    """Super Class representing a 'hut' building tile"""

    NON_FOOD_TYPES = [Resource.wood, Resource.clay, Resource.stone, Resource.gold, Resource.joker]
    RESOURCE_TYPES = [Resource.wood, Resource.clay, Resource.stone, Resource.gold]
    
    def __init__(self):
        self.player = None

    def placePerson(self, player):
        if self.isOccupied():
            from Board import PlacementError
            raise PlacementError("hut is already occupied")
        self.player = player

    def removePerson(self):
        self.player = None

    def isOccupied(self):
        return self.player != None

    def isOccupiedBy(self):
        return self.player
    
    def value(self):
        return sum(self._costs)
    
    def containsOnlyFood(self, resources):
        return sum([resources.count(resourceType) for resourceType in self.NON_FOOD_TYPES]) == 0
        
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
        while Resource.joker in clone:
            clone.remove(Resource.joker)
            missing.pop()
        return missing

    def __str__(self):
        suffix = self.isOccupied() and self.player.getOutputAbr() or ""
        return str(self._costs) + suffix
    
class AnyHut(Hut):
    """ 1-7 Hut """
    def __init__(self):
        Hut.__init__(self)
        self._costs = []

    def costs(self, resources):
        nonFood = [self.make_jokers_gold(resource) for resource in resources if resource != Resource.food]
        self._costs = nonFood[:7]
        return nonFood[:7]

    def make_jokers_gold(self, resource):
        return Resource.gold if resource == Resource.joker else resource
        
    def missing(self, resources):
        if len(resources) == 0 or self.containsOnlyFood(resources) :
            return [Resource.wood]
        return [] 
    
    def __str__(self):
        suffix = self.isOccupied() and self.player.getOutputAbr() or ""        
        return "[any:1-7]"  + suffix
    
class CountHut(Hut):
    """ Hut with four or five resources of 1 to 4 different types"""
    
    def __init__(self, resourceCount, typesCount):
        Hut.__init__(self)
        self.resourceCount = resourceCount
        self.typesCount = typesCount
        self._costs = []

    def getResourceCount(self):
        return self.resourceCount

    def costs(self, resources):
        result = []        
        nonFood = [resource for resource in resources if resource in self.NON_FOOD_TYPES]
        if self.missing (resources):
            return result

        availableTypes = self.extractAvailableResourceTypes(resources)
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

    def sufficientResources(self, nonFood, typesPaymentCandidate):
        neededResourceCount = self.resourceCount - nonFood.count(Resource.joker)
        return sum([nonFood.count(resourceType) for resourceType in typesPaymentCandidate]) >= neededResourceCount

    def tooFewDifferentTypes(self, typesCounts, jokerCount):
        return (4 - typesCounts.count(0)) + jokerCount < self.typesCount

    def tooFewResources(self, resources):
        availableTypes = self.extractAvailableResourceTypes(resources)
        for permutation in permutations(availableTypes, self.typesCount):
            if self.sufficientResources(resources, permutation):
                return False
        return True

    def extractAvailableResourceTypes(self, resources):
        return [resourceType for resourceType in self.RESOURCE_TYPES if resources.count(resourceType) > 0]
    
    def extractTypeCounts(self, resources):
        return [resources.count(resourceType) for resourceType in self.RESOURCE_TYPES] 

    def missing(self, resources):
        if len(resources) == 0 or self.containsOnlyFood(resources):
            necessaryTypes = self.RESOURCE_TYPES[:self.typesCount] 
            return necessaryTypes + self.allWood(self.resourceCount - self.typesCount)
        
        typeCounts = self.extractTypeCounts(resources)
        
        if self.tooFewDifferentTypes(typeCounts, resources.count(Resource.joker)):
            result = self.findMissingResourceTypes(typeCounts, resources.count(Resource.joker))
            return result + self.allWood(self.resourceCount - (sum(typeCounts) + resources.count(Resource.joker) + len(result)))
          
        if self.tooFewResources(resources):
            availableTypes = self.extractAvailableResourceTypes(resources)
            if len(availableTypes) == 0:
                availableTypes.append(Resource.wood)
            firstPossibleTypes = availableTypes[:self.typesCount]
            clone = resources[:]
            for jokerCount in range(resources.count(Resource.joker)):
                clone.append(firstPossibleTypes[0])
            return (self.resourceCount - sum([clone.count(resourceType) for resourceType in firstPossibleTypes])) * [firstPossibleTypes[0]] 
        return []
    
    def findMissingResourceTypes(self, typeCounts, jokerCount):
        """ returns list with missing Resource types in typeCounts """
        
        missingTypesCount =  self.typesCount - ((4 - typeCounts.count(0)) + jokerCount)
        result = []
 
        if missingTypesCount <= 0:
            return result
        
        for idx, count in enumerate(typeCounts):
            if count == 0:
                result.append(Resource.from_value(idx + 3))
                missingTypesCount -= 1
            if missingTypesCount == 0:
                return result
            
        raise BaseException("findMissingResourceTypes called with illegal typeCounts: %s" % str(typeCounts))
    
    def allWood(self, count):
        """ returns list with all count wood resources """
        
        return count * [Resource.wood]
        
    def __str__(self):
        suffix = self.isOccupied() and self.player.getOutputAbr() or ""        
        return "[any:%d, types:%d]" %(self.resourceCount, self.typesCount)  + suffix

def main():
    print("hubba")

if __name__ == '__main__':
    main()
