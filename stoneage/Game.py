#! /usr/bin/env python3

class Game:
    """Class responsible for the game bookkeeping"""
    
    def __init__(self):
        pass

    def isFinished(self):
        return False

    def getBuildingTiles(self):
        return [7 * ["hut"] for r in range(0, 4)]

def main():
    pass

if __name__ == '__main__':
    main()
