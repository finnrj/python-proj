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

   
    def __init__(self):
        self.board = Board()
        self.players = []
        
    def playerCount(self):
        return len(self.players)
    
    def addPlayer(self, player):
        self.players.append(player)
    
    def allPersonsPlaced(self):
        return sum([player.personsLeft(self.board) for player in self.players]) == 0
    
    def processRound(self, round):
        for player in self.players:
            player.newRound()
        print("\nRound: %d" % (round))
        while not self.allPersonsPlaced():
            for player in [p for p in self.players if p.personsLeft(self.board) > 0]:
                print("Player: %-6s to place persons" % (player.getOutputColor()))                
                if isinstance(player.strategy, Human):                
                    print (self.board)  
                player.placePersons(self.board)

        for player in self.players: # reap resources and buy building tiles
            print("Player: %-6s evaluates" % (player.getOutputColor()))
            if isinstance(player.strategy, Human):
                print (self.board)

        for idx, player in enumerate(self.players): # reap resources and buy building tiles
            print (self.board)
            huts = self.board.reapResources(self.players[idx:] + self.players[:idx])
            
            boughtHuts = player.buyHuts(huts)
            self.board.popHuts(boughtHuts)
            print(player)
        
        for player in self.players: # feed and adjust score
            player.feed()
        
        self.players = self.players[1:] + self.players[:1]  

    def finished(self):
        return self.board.isFinished()
    
    def getPlayers(self):
        return sorted(self.players[:], reverse = True)
    
    def printPlayers(self):
        maximalLength = max(len(player.getOutputColor()) for player in self.players)
        print("Players:")
        for player in self.getPlayers():
            print(("%-" + str(maximalLength) + "s: %s") % (player.getOutputColor(), player.getStrategy()))

    def printScores(self):
        maximalLength = max(len(player.getOutputColor()) for player in self.players)
        print("Scores:")
        for player in self.getPlayers():
            print(("%-" + str(maximalLength) + "s: %3d") % (player.getOutputColor(), player.getScore()))

    def printFinalScores(self):
        maximalLength = max(len(player.getOutputColor()) for player in self.players)
        print("\n\nFinal scores:")
        for player in self.getPlayers():
            print(("%-" + str(maximalLength) + "s: %3d, second criteria: %2d") % (player.getOutputColor(), player.getScore(), player.secondScoreCriteria()))


def main():
    game = Game()
    game.addPlayer(Player("Red", StupidBot()))
    game.addPlayer(Player("Blue",  StupidBot()))
    game.addPlayer(Player("Green",  Human()))
    game.addPlayer(Player("Yellow",  StupidBot()))
    shuffle(game.players)
    game.printPlayers()
    round = 1
    try:
        while not game.finished():
            input("Press the return key to proceed to the next round....")
            game.processRound(round)
            round +=1
            game.printScores()
        game.printFinalScores()
    except KeyboardInterrupt:
        game.printFinalScores()     
        print("\nbye and see you soon!")

if __name__ == '__main__':
    main()
