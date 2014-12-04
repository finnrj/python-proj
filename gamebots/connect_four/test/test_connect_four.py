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
        self.assertTrue(self.board.is_empty())
        self.board.play(3)
        self.assertFalse(self.board.is_empty())
        
    def test_move_position(self):
        self.assertIsNone(self.board.get_color(0, 3))
        self.board.play(3)
        self.assertEqual(0, self.board.get_color(0, 3))
        self.board.play(2)
        self.assertEqual(1, self.board.get_color(0, 2))
        self.board.play(3)
        self.assertEqual(0, self.board.get_color(1, 3))
        
    def test_column_filled_up(self):
        self.assertEqual(0, self.board.get_player())
        self.board.play(3)
        
        self.assertEqual(1, self.board.get_player()) 
        self.board.play(3)
        
        self.assertEqual(0, self.board.get_player())
        self.board.play(3)
        
        self.assertEqual(1, self.board.get_player())
        self.board.play(3)
        
        self.assertEqual(0, self.board.get_player())
        self.board.play(3)
        
        self.assertEqual(1, self.board.get_player())
        self.board.play(3)
        
        self.assertEqual(0, self.board.get_player())
        self.board.play(3)
        
        self.assertEqual(0, self.board.get_player())
        
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
        
    def test_column_of_move(self):
        self.board.play(7)
        self.assertTrue(self.board.is_empty())
        self.board.play(-1)
        self.assertTrue(self.board.is_empty())
        self.board.play("1")
        self.assertTrue(self.board.is_empty())
    
    def test_full_board(self):
        self.fill_board_without_winner()
        self.assertIsNone(self.board.get_winner())
        self.assertTrue(self.board.game_is_over())
    
    def fill_board_without_winner(self):
        for x in range(self.board.colCount()):
            if x == 3: continue
            for y in range(self.board.rowCount()):
                self.board.play(x)
        self.board.board[3][0]=1
        for y in range(self.board.rowCount() - 1):
            self.board.play(3)
        self.board.move_count+=1
        
    def test_player_0_has_winning_diagonal(self):
        self.board.board[0][0]=0
        self.board.board[1][1]=0
        self.board.board[2][2]=0
        self.board.board[3][3]=0
        self.assertEqual(0, self.board.get_winner())

    def test_player_0_has_winning_diagonal2(self):
        self.board.board[5][5]=0
        self.board.board[4][4]=0
        self.board.board[3][3]=0
        self.board.board[2][2]=0
        self.assertEqual(0, self.board.get_winner())
        
    def test_player_0_has_winning_diagonal3(self):
        self.board.board[1][0]=0
        self.board.board[2][1]=0
        self.board.board[3][2]=0
        self.board.board[4][3]=0
        self.assertEqual(0, self.board.get_winner())

    def test_player_0_has_winning_diagonal4(self):
        self.board.board[3][0]=0
        self.board.board[4][1]=0
        self.board.board[5][2]=0
        self.board.board[6][3]=0
        self.assertEqual(0, self.board.get_winner())
    
    def test_player_0_has_winning_diagonal5(self):
        self.board.board[0][3]=0
        self.board.board[1][2]=0
        self.board.board[2][1]=0
        self.board.board[3][0]=0
        print(self.board)
        self.assertEqual(0, self.board.get_winner())
        
    def test_clone_empty_board(self):
        cloned_board = self.board.clone()
        self.assertTrue(cloned_board.is_empty())
        cloned_board.play(1)
        self.assertTrue(self.board.is_empty())
        self.assertFalse(cloned_board.is_empty())

    def test_clone_board(self):
        self.board.play(1)
        cloned_board = self.board.clone()
        self.assertFalse(cloned_board.is_empty())
        self.assertEqual(self.board.move_count, cloned_board.move_count)
        
        cloned_board.play(1)
        self.assertEqual(self.board.move_count + 1, cloned_board.move_count)

    def test_clone_board_column(self):
        self.assertTrue(self.board.is_empty())
        cloned_board = self.board.clone()
        cloned_board.play(1)
        self.assertIsNone(self.board.board[1][0])

if __name__ == "__main__":
#     suite = unittest.TestLoader().loadTestsFromTestCase(Test)
#     unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()
