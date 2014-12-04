#! /usr/bin/python3
'''
Created on Nov 27, 2014

@author: finn
'''
from connect_four.board import Board
from random import randint
import sys
from sys import argv
from connect_four.monte_carlo import MonteCarloIterative

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

def play_with_ai(ai=None):
    board = Board(6, 7)
    while not board.game_is_over():
        play_ai(board, ai)
        print(board)
        if not board.game_is_over():
            board.play(input_move())

    print(board)    
    print("the winner is %s" % board.get_winner())

def play_ai_against_ai(ai_with_color0, ai_with_color1):        
    board = Board(6, 7)
    while not board.game_is_over():
        play_ai(board, ai_with_color0)
        print(board)
        play_ai(board, ai_with_color1)
        print(board)
        
    print(board)    
    print("the winner is %s" % board.get_winner())
        
def play_ai(board, ai):
    if board.game_is_over():
        return 
    
    if not ai:
        board.play(randint(0, 6))
    else:
        board.play(ai.play(board))


# def play_with_stupid_ai_game():
#     board = Board(6, 7)
#     while not board.game_is_over():
#         board.play(randint(0, 6))
#         print(board)
#         board.play(input_move())
# 
#     print(board)    
#     print("the winner is %s" % board.get_winner())
# 
# def play_with_iterative_Monty():
#     board = Board(6, 7)
#     monty = MonteCarloIterative()
#     monty100 = MonteCarloIterative(100)   
#     while not board.game_is_over():
#         board.play(monty.play(board))
#         print(board)
#         board.play(monty100.play(board))        
# #         board.play(input_move())
#     print(board)    
#     print("the winner is %s" % board.get_winner())
# 
# def play_a_game():
#     board = Board(6, 7)
#     while not board.game_is_over():
#         board.play(randint(0, 6))
# #     if board.get_winner() is None:
#     print(board)    
#     print("the winner is %s" % board.get_winner())
    
if __name__ == "__main__":
    number_of_games = int(argv[1]) if len(argv) > 1 else 1
    for game in range(number_of_games):
        print("game: %d" % (game + 1))
#         play_a_game()
#         play_with_stupid_ai_game()
        play_with_ai(MonteCarloIterative(100))
        input("bye!")
    print("finished!")
