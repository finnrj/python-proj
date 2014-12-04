'''
Created on Nov 27, 2014

@author: finn
'''
import unittest
from connect_four.monte_carlo import MonteCarloIterative
from connect_four.board import Board


class Test(unittest.TestCase):


    def setUp(self):
        unittest.TestCase.setUp(self)
        self.monty = MonteCarloIterative()
        self.monty.color = 1

    def test_move(self):
        board=Board(6,7)
        move = self.monty.play(board)
        self.assertTrue(move in range(7))
        
    def test_add_score(self):
        column = 0
        self.monty.add_score(column, 0)
        self.assertEqual(-1, self.monty.score(column))

    def test_play_one_round(self):
        board = Board(6, 7)
        played_move = self.monty.play(board)
        self.assertTrue(played_move in range(7))

    def test_add_score_for_other_color(self):
        self.monty.color = 0
        column = 0
        self.monty.add_score(column, self.monty.color)
        self.assertEqual(1, self.monty.score(column))

    def test_add_score2(self):
        column = 0
        self.monty.add_score(column, self.monty.color)
        self.assertEqual(1, self.monty.score(column))
        
    def test_add_score3(self):
        column = 0
        self.monty.add_score(column, None)
        self.assertEqual(0, self.monty.score(column))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()