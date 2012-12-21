#! /usr/bin/env python3

class Hut:
    """Class representing a 'hut' building tile"""
    
    def __init__(self, r1, r2, r3):
        self._costs = [r1, r2, r3]
        self._occupied = False

    def costs(self):
        return self._costs[:]

    def missing(self, resources):
        clone = resources[:]
        missing = []
        for res in self._costs:
            try:
                clone.remove(res)
            except:
                missing.append(res)
        return missing
    
    def placePerson(self):
        self._occupied = True

    def removePerson(self):
        if self._occupied:
            self._occupied = False

    def isOccupied(self):
        return self._occupied

def main():
    pass

if __name__ == '__main__':
    main()
