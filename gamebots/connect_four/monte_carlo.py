'''
Created on Nov 27, 2014

@author: finn
'''

class MonteCarlo:
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
#                     self.play_to_end(clone)
                    self.add_score(col, clone.get_winner())
        return self.scores.index(max(self.scores))
    
    def score(self, col):
        return 10

    
    def add_score(self, col, winner):
        if winner==self.color:
            self.scores[col]+=1
        elif winner is not None:
            self.scores[col]-=1
    
    
    
