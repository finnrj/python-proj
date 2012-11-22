'''
Created on Nov 22, 2012

@author: finn
'''

class Game(object):
    '''
    class to represent the game loop
    '''

    players = []
    
    def __init__(self):
        pass
        
    def playerCount(self):
        return len(self.players)
    
    def addPlayer(self, player):
        self.players.append(player)
