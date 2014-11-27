'''
Created on Nov 27, 2014

@author: finn
'''
import unittest
from connect_four.monte_carlo import MonteCarlo
from connect_four.board import Board


class Test(unittest.TestCase):


    def test_move(self):
        board=Board(6,7)
        monty=MonteCarlo()
        move = monty.play(board)
        self.assertTrue(move in range(7))
        
#     def test_move_possible(self):
#         board=Board(6,7)
#         for num in range(6):
#             board.play(0)
#             
#         monty=MonteCarlo()
#         move = monty.play(board)
#         self.assertTrue(move in range(1,7))
    
#     def test_winning_position_1(self):
#         board=Board(6,7)
#         board.board[0][0] = 1
#         board.board[1][0] = 1
#         board.board[2][0] = 1
#         board.play(4)
#         print(board)
#             
#         monty=MonteCarlo(9)
#         monty.play(board)
#         self.assertEqual(9, monty.score(3)) 
#         
#     def test_winning_position_2(self):
#         board=Board(6,7)
#         board.board[0][0] = 1
#         board.board[0][1] = 1
#         board.board[0][2] = 1
#         board.play(1)
#         print(board)
#             
#         monty=MonteCarlo(10)
#         monty.play(board)
#         self.assertEqual(10, monty.score(0)) 

    def test_add_score(self):
        monty=MonteCarlo()
        monty.color = 1
        
        monty.add_score(0, 0)
        self.assertEqual(-1, monty.scores[0])

    def test_add_score2(self):
        monty=MonteCarlo()
        monty.color = 1
        
        monty.add_score(0, 1)
        self.assertEqual(1, monty.scores[0])


    def test_add_score3(self):
        monty=MonteCarlo()
        monty.color = 1
        
        monty.add_score(0, None)
        self.assertEqual(0, monty.scores[0])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()