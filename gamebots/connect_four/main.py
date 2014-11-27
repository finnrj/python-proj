'''
Created on Nov 27, 2014

@author: finn
'''
from connect_four.board import Board
from random import randint
import sys
from sys import argv

def input_move():
    column=None
    while column not in range(7):
        try:
            input_str=input("pick a column to play (0-6): ")
            if input_str=="q":
                sys.exit()
            column = int(input_str)
        except ValueError:
            pass
        
    return column

def play_with_ai_game():
    board = Board(6, 7)
    while not board.game_is_over():
        board.play(randint(0, 6))
        print(board)
        board.play(input_move())

    print(board)    
    print("the winner is %s" % board.get_winner())

def play_a_game():
    board = Board(6, 7)
    while not board.game_is_over():
        board.play(randint(0, 6))
#     if board.get_winner() is None:
    print(board)    
    print("the winner is %s" % board.get_winner())
    
if __name__ == "__main__":
    number_of_games = int(argv[1]) if len(argv) > 1 else 10
    for game in range(number_of_games):
        print("game: %d" % (game + 1))
#         play_a_game()
        play_with_ai_game()
        input("bye!")
    print("finished!")
