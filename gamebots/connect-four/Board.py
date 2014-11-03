'''
Created on Oct 30, 2014

@author: finn
'''

class Board:

    def __init__(self, rows, cols):
        self.board= [[None for row in range(rows)] for col in range(cols)]
        self.move_count=0
    
    def colCount(self):
        return len(self.board)
    
    def rowCount(self):
        return len(self.board[0])
    
    def isEmpty(self):
        return self.move_count == 0
    
    def play(self, column):
        idx = self.board[column].index(None)
        self.board[column][idx] = self.move_count % 2
        self.move_count += 1
    
    def getColor(self, row, column):
        return self.board[column][row]
    
    def getMarker(self, row, column):
        return "-" if self.board[column][row] is None else self.board[column][row]
                    
    def __str__(self):
        strings = ["\n"]
        strings.append((4 * " ") + "".join([("%2s" % col) for col in range(self.colCount())]))
        strings.append((2 + self.colCount()) * "==")
        for row in reversed(range(self.rowCount())):
            strings.append(("%2s" % row) + ("%2s" % " |")\
             + "".join(["%2s" % self.getMarker(row, col) for col in range(self.colCount())]))
        return "\n".join(strings) 
        
    
    
    
    
    
    
    
    
    