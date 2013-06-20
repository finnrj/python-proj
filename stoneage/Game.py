#! /usr/bin/env python3

'''
Created on Nov 22, 2012

@author: finn
'''

from Board import Board
from random import shuffle
from Strategy import StupidBot, Human
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
    
    def allPersonsPlaced(self):
        return sum([player.personsLeft(self.board) for player in self.players]) == 0
    
    def processRound(self, round):
        print("\nRound: %d" % (round))
        while not self.allPersonsPlaced():
            for player in [p for p in self.players if not self.board.personCount(p.playerAbr) == p.personCount]:
                print("Player: %s to place persons" % (player.getColor()))                
                print (self.board)
                player.placePersons(self.board)

        for player in self.players: # reap resources and buy building tiles
            print("Player: %s evaluates" % (player.getColor()))
            print (self.board)
            resources, huts = self.board.reapResources(player)
            player.addResources(resources)
            
            boughtHuts = player.buyHuts(huts)
            self.board.popHuts(boughtHuts)
                
            #player.addHuts(huts)
            print(player)
        
        for player in self.players: # feed and adjust score
            player.feed()
        
        self.players = self.players[1:] + self.players[:1]  

    def finished(self):
        return self.board.isFinished()
    
    def printPlayers(self):
        print("Players:")
        for player in self.players:
            print("%-7s" % player.getColor(), ":", player.getStrategy())
    
    def position(self):
        return """Available huts: %s
         
%s""" % (" ".join([str(hut) for hut in self.board.availableHuts()]), "\n\n".join([player.asString() for player in self.players]))


def main():
    game = Game()
    game.addPlayer(Player("Red", StupidBot()))
    game.addPlayer(Player("Blue",  StupidBot()))
    game.addPlayer(Player("Yellow",  Human()))
    shuffle(game.players)
    game.printPlayers()
    round = 1
    try:
        while not game.finished():
            input("Press the return key to proceed to the next round....")
            game.processRound(round)
            round +=1
        for player in game.players:
            print("\nPlayer %s final score: %d" % (player.getColor() , player.finalScore()))
    except KeyboardInterrupt:
        print("bye")
    

if __name__ == '__main__':
    main()