#! /usr/bin/env python3

from BuildingTile import BuildingTile
from random import shuffle

class Board:
    """Class representing the gameboard """

    tiles = [BuildingTile(3,3,4),
             BuildingTile(3,3,5),
             BuildingTile(3,3,6),
             BuildingTile(3,4,5),
             BuildingTile(3,4,4),
             BuildingTile(3,5,5),
             BuildingTile(3,4,6),
             BuildingTile(3,4,6),
             BuildingTile(3,4,5),
             BuildingTile(3,5,6),
             BuildingTile(3,5,6),
             BuildingTile(4,4,5),
             BuildingTile(4,4,6),
             BuildingTile(4,5,5),
             BuildingTile(4,5,6),
             BuildingTile(4,5,6),
             BuildingTile(5,5,6)
             ]
    
    def __init__(self):
        shuffle(Board.tiles)
        self.tileStacks = [Board.tiles[0:4],
                            Board.tiles[4:8],
                            Board.tiles[8:12],
                            Board.tiles[12:]]

    def numberOfBuildingTilesLeft(self):
        return [len(stack) for stack in self.tileStacks]

    def availableBuildingTiles(self):
        return [stack[-1] for stack in self.tileStacks]

def main():
    pass

if __name__ == '__main__':
    main()
