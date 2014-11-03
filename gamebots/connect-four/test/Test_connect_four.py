'''
Created on Oct 30, 2014

@author: finn
'''
import unittest
from Board import Board


class Test(unittest.TestCase):

    def setUp(self):
        self.board=Board(6, 7)
        
    def test_board_initialisation_rows(self):
        self.assertEqual(6, self.board.rowCount())
        
    def test_board_initialisation_columns(self):
        self.assertEqual(7, self.board.colCount())

    def test_move_count(self):
        self.assertTrue(self.board.isEmpty())
        self.board.play(3)
        self.assertFalse(self.board.isEmpty())
        
    def test_move_position(self):
        self.assertIsNone(self.board.getColor(0, 3))
        self.board.play(3)
        self.assertEqual(0, self.board.getColor(0, 3))
        self.board.play(2)
        self.assertEqual(1, self.board.getColor(0, 2))
        self.board.play(3)
        print(self.board)   
        self.assertEqual(0, self.board.getColor(1, 3))

if __name__ == "__main__":
#     suite = unittest.TestLoader().loadTestsFromTestCase(Test)
#     unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()