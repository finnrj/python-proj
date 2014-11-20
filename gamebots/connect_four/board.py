#! /usr/bin/python3
'''
Created on Oct 30, 2014

@author: finn


'''
from random import randint
from sys import argv

class Board:

    def __init__(self, r, c):
        self.board = [[None for row in range(r)] for col in range(c)]
        self.move_count = 0
    
    def colCount(self):
        return len(self.board)
    
    def rowCount(self):
        return len(self.board[0])
    
    def isEmpty(self):
        return self.move_count == 0
    
    def play(self, col):
        if self.is_col_full(col):
            return
        self.board[col][self.board[col].index(None)] = self.getPlayer()
        self.move_count += 1
        
    def is_col_full(self, col):
        return not None in self.board[col]
    
    def getColor(self, row, col):
        return self.board[col][row]
    
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
        for board_type in (self.board, self.get_transposed_board(), self.get_diagonal_board()):
            for column in board_type:
                winning_color = self.four_connected_in_col(column)
                if winning_color is not None:
                    return winning_color

        return None
    
    def get_diagonal_board(self):
        return [
                 [self.board[r][r - 1] for r in range(1, 7)],
                 [self.board[r][r - 2] for r in range(2, 7)],
                 [self.board[r][r - 3] for r in range(3, 7)],
                 [self.board[r][r + 0] for r in range(0, 6)],
                 [self.board[r][r + 1] for r in range(0, 5)],
                 [self.board[r][r + 2] for r in range(0, 4)],
                 [self.board[r][(3 - r)] for r in range(0, 4)],
                 [self.board[r][(4 - r)] for r in range(0, 5)],
                 [self.board[r][(5 - r)] for r in range(0, 6)],
                 [self.board[r][(6 - r + 0)] for r in range(1, 7)],
                 [self.board[r][(6 - r + 1)] for r in range(2, 7)],
                 [self.board[r][(6 - r + 2)] for r in range(3, 7)],
                ]
   
    def get_transposed_board(self):
        return [[x[idx] for x in self.board] for idx in range(self.rowCount())]

    def game_is_over(self):
        return self.get_winner() is not None or self.move_count == 42
    
    def __str__(self):
        strings = [""]
        for row in reversed(range(self.rowCount())):
            strings.append(("%2s" % row) + ("%2s" % " |")\
             + "".join(["%2s" % self.getMarker(row, col) for col in range(self.colCount())]))
        strings.append((2 + self.colCount()) * "--")
        strings.append(4 * " " + "".join([("%2s" % col) for col in range(self.colCount())]))
        return "\n".join(strings) 

def play_a_game():
    board = Board(6, 7)
    while not board.game_is_over():
        board.play(randint(0, 6))
#     if board.get_winner() is None:
    print(board)    
    print("the winner is %s" % board.get_winner())
    
if __name__ == "__main__":
    number_of_games = argv[1] if len(argv) > 1 else 10
    for game in range(number_of_games):
        print("game: %d" % (game + 1))
        play_a_game()
        input(" ")
    print("finished!")
    
    
    
    
    
    
    
    
