'''
Created on Oct 30, 2014

@author: finn
'''
import unittest
from connect_four import board

class Test(unittest.TestCase):

    def setUp(self):
        self.board=board.Board(6, 7)
        
    def test_board_initialisation(self):
        self.assertEqual(6, self.board.rowCount())
        self.assertEqual(7, self.board.colCount())
        self.assertIsNone(self.board.get_winner())
        self.assertFalse(self.board.game_is_over())  

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
        self.assertEqual(0, self.board.getColor(1, 3))
        
    def test_column_filled_up(self):
        self.assertEqual(0, self.board.getPlayer())
        self.board.play(3)
        
        self.assertEqual(1, self.board.getPlayer()) 
        self.board.play(3)
        
        self.assertEqual(0, self.board.getPlayer())
        self.board.play(3)
        
        self.assertEqual(1, self.board.getPlayer())
        self.board.play(3)
        
        self.assertEqual(0, self.board.getPlayer())
        self.board.play(3)
        
        self.assertEqual(1, self.board.getPlayer())
        self.board.play(3)
        
        self.assertEqual(0, self.board.getPlayer())
        self.board.play(3)
        
        self.assertEqual(0, self.board.getPlayer())
        
    def test_player_0_has_simple_winning_col(self):
        self.board.play(1)
        self.board.play(2)
        self.board.play(1)
        self.board.play(3)
        self.board.play(1)
        self.board.play(5)
        self.assertIsNone(self.board.get_winner())
        self.board.play(1)
        self.assertEqual(0, self.board.get_winner())
        
    def test_player_1_has_simple_winning_col(self):
        self.board.play(6)
        self.board.play(1)
        self.board.play(2)
        self.board.play(1)
        self.board.play(3)
        self.board.play(1)
        self.board.play(5)
        self.assertIsNone(self.board.get_winner())
        self.board.play(1)
        self.assertEqual(1, self.board.get_winner())
        self.assertTrue(self.board.game_is_over())

    def test_player_0_has_mixed_winning_col(self):
        self.board.play(1)
        self.board.play(1)
        
        self.board.play(1)
        self.board.play(3)
        self.board.play(1)
        self.board.play(5)
        self.board.play(1)
        self.board.play(5)

        self.assertIsNone(self.board.get_winner())
        self.board.play(1)
        self.assertEqual(0, self.board.get_winner())
        
    def test_player_0_has_winning_row(self):
        self.board.play(1)
        self.board.play(1)
        
        self.board.play(2)
        self.board.play(2)
        self.board.play(3)
        self.board.play(3)
        self.assertIsNone(self.board.get_winner())
        self.board.play(4)
        self.assertEqual(0, self.board.get_winner())
        
    def test_full_board(self):
        self.fill_board_without_winner()
        self.assertIsNone(self.board.get_winner())
        self.assertTrue(self.board.game_is_over())
        print(self.board)
    
    def fill_board_without_winner(self):
        for x in range(self.board.colCount()):
            if x == 3: continue
            for y in range(self.board.rowCount()):
                self.board.play(x)
        self.board.board[3][0]=1
        for y in range(self.board.rowCount() - 1):
            self.board.play(3)
        self.board.move_count+=1
    

if __name__ == "__main__":
#     suite = unittest.TestLoader().loadTestsFromTestCase(Test)
#     unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()
