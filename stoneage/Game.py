#! /usr/bin/env python3

'''
Created on Nov 22, 2012

@author: finn
'''

from Board import Board
from Player import Player

class Game(object):
    '''
    class to represent the game loop
    '''

    players = []
    
    def __init__(self):
        self.board = Board()
        
    def playerCount(self):
        return len(self.players)
    
    def addPlayer(self, player):
        self.players.append(player)
        
    def processRound(self):
        while self.board.personCount() < 5:
            for player in self.players: 
                player.placePersons(self.board)
        for player in self.players: # reap resources and buy building tiles
            resources, huts = self.board.reapResources()
            player.addResources(resources)
            player.addHuts(huts)
        for player in self.players: # feed and adjust score
            player.feed()

    def finished(self):
        return self.board.isFinished()
    
    def position(self):
        return """Available huts: %s 
%s""" % (" ".join([hut.toString() for hut in self.board.availableHuts()]), "\n".join([player.toString() for player in self.players]))

def main():
    game = Game()
    game.addPlayer(Player())
    try:
        while not game.finished():
            input("waiting...")
            game.processRound()
            print(game.position())
    except KeyboardInterrupt:
        print("bye")
    

if __name__ == '__main__':
    main()