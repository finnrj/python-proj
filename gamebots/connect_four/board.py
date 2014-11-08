'''
Created on Oct 30, 2014

@author: finn
'''

class Board:

    def __init__(self, y, x):
        self.board= [[None for row in range(y)] for col in range(x)]
        self.move_count=0
    
    def colCount(self):
        return len(self.board)
    
    def rowCount(self):
        return len(self.board[0])
    
    def isEmpty(self):
        return self.move_count == 0
    
    def play(self, x):
        if self.is_col_full(x):
            return
        self.board[x][self.board[x].index(None)] = self.getPlayer()
        self.move_count += 1
        
    def is_col_full(self, x):
        return not None in self.board[x]
    
    def getColor(self, x, y):
        return self.board[y][x]
    
    def getMarker(self, y, x):
        return "-" if self.board[x][y] is None else self.board[x][y]
                    
    def getPlayer(self):
        return self.move_count % 2
    
    def four_connected_in_col(self, x):
        for start in range(len(x) - 3):
            colors = set(x[start:start + 4])
            if len(colors) == 1 and not None in colors:
                return colors.pop()
 
        return None
    
    def get_winner(self):
        for board_type in (self.board, self.get_transposed_board()):
            for column in board_type:
                winning_color = self.four_connected_in_col(column)
                if winning_color is not None:
                    return winning_color

        return None
   
    def get_transposed_board(self):
        return [[x[idx] for x in self.board] for idx in range(self.rowCount())]

    def game_is_over(self):
        return self.get_winner() is not None or self.move_count==42
    
    def __str__(self):
        strings = ["\n"]
        strings.append((4 * " ") + "".join([("%2s" % col) for col in range(self.colCount())]))
        strings.append((2 + self.colCount()) * "==")
        for row in reversed(range(self.rowCount())):
            strings.append(("%2s" % row) + ("%2s" % " |")\
             + "".join(["%2s" % self.getMarker(row, col) for col in range(self.colCount())]))
        return "\n".join(strings) 
    
    
    
    
    
    
    
    
    
    