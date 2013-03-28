#! /usr/bin/env python3

'''
Created on Nov 22, 2012

@author: finn
'''

from Board import Board
from Player import Player, HumanPlayer
from random import shuffle

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
    
    def allPersonsPlaced(self):
        return sum([player.personsLeft(self.board) for player in self.players]) == 0
    
    def processRound(self, round):
        print("\nRound: %d" % (round))
        while not self.allPersonsPlaced():
            for player in self.players: 
                print (self.board.toString())
                print("Player: %s to place persons\n" % (player.getColor()))                
                player.placePersons(self.board)

        for player in self.players: # reap resources and buy building tiles
            print (self.board.toString())
            print("Player: %s evaluates\n" % (player.getColor()))
            resources, huts = self.board.reapResources(player.getAbr())
            player.addResources(resources)
            
            boughtHuts = player.buyHuts(huts)
            self.board.popHuts(boughtHuts)
                
            #player.addHuts(huts)
            print(player.toString())
        
        for player in self.players: # feed and adjust score
            player.feed()
        
        self.players = self.players[1:] + self.players[:1]  

    def finished(self):
        return self.board.isFinished()
    
    def position(self):
        return """Available huts: %s
         
%s""" % (" ".join([hut.hutAsString() for hut in self.board.availableHuts()]), "\n\n".join([player.hutAsString() for player in self.players]))


def main():
    game = Game()
    game.addPlayer(Player("Red"))
    game.addPlayer(Player("Blue"))
    game.addPlayer(HumanPlayer("Yellow"))
    shuffle(game.players)
    round = 1
    try:
        while not game.finished():
            input("waiting... (type return)\n")
            game.processRound(round)
            round +=1
        for player in game.players:
            print("\nPlayer %s final score: %d" % (player.getColor() , player.finalScore()))
    except KeyboardInterrupt:
        print("bye")
    

if __name__ == '__main__':
    main()