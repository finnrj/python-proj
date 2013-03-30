'''
Created on Mar 30, 2013

@author: finn
'''
import unittest
from Strategy import Strategy, StrategyNotImplemented, Human
from Player import Player
from Board import Board

class StrategyTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.human = Human()
        self.human.player = Player("Green", self.human)

    def testStrategyClassShouldBeImplemented(self):
        player = Player("Green", Strategy())
        with self.assertRaisesRegex(StrategyNotImplemented, "The placePersons\(\) method should be implemented"):
            player.placePersons(Board())

#    Hunting grounds
    def testHumanInputH3(self):
        self.human.processInput("h3", self.board)
        self.assertEqual(3, self.board.personsOnGrounds(self.human.player.getAbr()))

    def testHumanInputH5(self):
        self.human.processInput("h5", self.board)
        self.assertEqual(5, self.board.personsOnGrounds(self.human.player.getAbr()))

#    Forest
    def testHumanInputF3(self):
        self.assertEqual(0, 7 - self.board.freeForestSlots())
        self.human.processInput("f3", self.board)
        self.assertEqual(3, self.board.personsOnGrounds(self.human.player.getAbr()))
        self.assertEqual(3, 7 - self.board.freeForestSlots())
        
    def testHumanInputF5(self):
        self.assertEqual(0, 7 - self.board.freeForestSlots())
        self.human.processInput("f5", self.board)
        self.assertEqual(5, self.board.personsOnGrounds(self.human.player.getAbr()))
        self.assertEqual(5, 7 - self.board.freeForestSlots())

    def testHumanInputBuilding2(self):
        self.assertEqual(4, len(self.board.availableHuts()))
        self.human.processInput("b2", self.board)
        self.assertEqual(3, len(self.board.availableHuts()))
        
                         



        
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(StrategyTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
