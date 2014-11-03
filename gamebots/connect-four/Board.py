'''
Created on Oct 30, 2014

@author: finn
'''

class Board:

    def __init__(self, rows, cols):
        self.board= [[None for col in range(cols)] for row in range(rows)]
        self.move_count=0
    
    def colCount(self):
        return len(self.board[0])
    
    def rowCount(self):
        return len(self.board)
    
    def isEmpty(self):
        return self.move_count == 0
    
    def play(self, column):
        idx = self.board[column].index(None)
        self.board[column][idx] = self.move_count % 2
        self.move_count += 1
    
    def getColor(self, row, column):
        return self.board[column][row]
    
    def __str__(self):
        row_str = "\n"
        for row in range(1, self.rowCount()+1):
            for col in range(self.colCount()):
                row_str += " %4s" % self.board[row*(-1)][col].__str__()
            row_str += "\n"
        return row_str 
        
    
    
    
    
    
    
    
    
    