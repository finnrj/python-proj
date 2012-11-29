#! /usr/bin/env python3

'''
Created on Nov 22, 2012

@author: finn
'''

from symbol import try_stmt
from Board import Board

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
                player.placePersons()
        for player in self.players: # reap resources and buy building tiles
            pass
        for player in self.players: # feed and adjust score
            pass

        
    def finished(self):
        return False

def main():
    game = Game()
    try:
        while not game.finished():
            game.processRound()
            print("Game is running")
    except KeyboardInterrupt:
        print("bye")
    

if __name__ == '__main__':
    main()