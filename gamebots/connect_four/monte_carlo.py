'''
Created on Nov 27, 2014

@author: finn
'''
from random import randint

class MonteCarloIterative:
    '''
    classdocs
    '''

    def __init__(self, rounds = 10):
        self.rounds = rounds
        self.color = None
        self.scores= 7 * [0]
        
    def play(self, board):
        self.color = board.get_player()
        self.scores= board.colCount() * [0]
        for round in range(self.rounds):
            for col in range(7):
                if board.is_valid_column(col):
                    clone = board.clone()
                    clone.play(col)
                    self.play_to_end(clone)
                    self.add_score(col, clone.get_winner())
        return sorted([(val,idx) for idx,val in enumerate(self.scores) 
                       if board.is_valid_column(idx)], reverse=True)[0][1]

    def play_to_end(self, board):
        while not board.game_is_over():
            board.play(randint(0, 6))
    
    def score(self, col):
        return self.scores[col]
    
    def add_score(self, col, winner):
        if winner==self.color:
            self.scores[col]+=1
        elif winner is not None:
            self.scores[col]-=1
    
    
    
