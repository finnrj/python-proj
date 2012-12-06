#! /usr/bin/env python3

class Hut:
    """Class representing a 'hut' building tile"""
    
    def __init__(self, r1, r2, r3):
        self.costs = [r1, r2, r3]
        self.occupied = False

    def missing(self, resources):
        clone = resources[:]
        missing = []
        for res in self.costs:
            try:
                clone.remove(res)
            except:
                missing.append(res)
        return missing
    
    def placePerson(self):
        self.occupied = True

    def isOccupied(self):
        return self.occupied

def main():
    pass

if __name__ == '__main__':
    main()
