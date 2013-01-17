#! /usr/bin/env python3

class Hut:
    """Class representing a 'hut' building tile"""
    
    def __init__(self):
        self.occupied = False

    def placePerson(self):
        self.occupied = True

    def removePerson(self):
        if self.occupied:
            self.occupied = False

    def isOccupied(self):
        return self.occupied
    
    def toString(self):
        return str(self._costs)
    
    def value(self):
        return sum(self._costs)
    
class SimpleHut(Hut):
    def __init__(self, r1, r2, r3):
        Hut.__init__(self)
        self._costs = [r1, r2, r3]

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
    
class AnyHut(Hut):
    def __init__(self):
        Hut.__init__(self)
        self._costs = []

    def costs(self, resources):
        nonFood = [resource for resource in resources if resource != 2]
        self._costs = nonFood[:7]
        return nonFood[:7]
        
    def missing(self, resources):
        if len(resources) == 0 or self.onlyFood(resources) :
            return [3]
        return [] 

    def onlyFood(self, resources):
        return sum([resources.count(num) for num in [3,4,5,6]]) == 0
    
class CountHut(Hut):
    def __init__(self):
        Hut.__init__(self)


def main():
    pass

if __name__ == '__main__':
    main()
