'''
Created on Mar 30, 2013

@author: finn
'''
import unittest
from Strategy import Strategy, StrategyNotImplemented, Human
from Player import Player
from Board import Board
from Toolbox import Toolbox

class HumanStrategyTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.human = Human()
        self.player = Player("Green", self.human)
        self.human.player = self.player

    def testStrategyClassShouldBeImplemented(self):
        player = Player("Green", Strategy())
        with self.assertRaisesRegex(StrategyNotImplemented, "The placePersons\(\) method should be implemented"):
            player.placePersons(Board())

#    Hunting grounds
    def testHumanInputH3(self):
        self.human.processPlacePersonsInput("f", 3,self.player.getAbr(), self.board)
        self.assertEqual(3, self.board.personsOnGrounds(self.human.player.getAbr()))

    def testHumanInputH5(self):
        self.human.processPlacePersonsInput("f", 5, self.player.getAbr(), self.board)
        self.assertEqual(5, self.board.personsOnGrounds(self.human.player.getAbr()))

#    Forest
    def testHumanInputF3(self):
        self.assertEqual(0, 7 - self.board.freeForestSlots())
        self.human.processPlacePersonsInput("w", 3, self.player.getAbr(), self.board)
        self.assertEqual(3, self.board.personsOnGrounds(self.human.player.getAbr()))
        self.assertEqual(3, 7 - self.board.freeForestSlots())
        
    def testHumanInputF5(self):
        self.assertEqual(0, 7 - self.board.freeForestSlots())
        self.human.processPlacePersonsInput("w", 5, self.player.getAbr(), self.board)
        self.assertEqual(5, self.board.personsOnGrounds(self.human.player.getAbr()))
        self.assertEqual(5, 7 - self.board.freeForestSlots())

    def testHumanInputBuilding2(self):
        self.assertEqual(4, len(self.board.availableHuts()))
        self.human.processPlacePersonsInput("h", 2, self.player.getAbr(), self.board)
        self.assertEqual(3, len(self.board.availableHuts()))
        
    def testHumanInputfarm(self):
        self.assertFalse(self.board.farmOccupied())
        self.human.processPlacePersonsInput("a", 1, self.player.getAbr(), self.board)
        self.assertEqual(1, self.board.personsOnGrounds(self.human.player.getAbr()))
        self.assertTrue(self.board.farmOccupied())
        
    def testHumanToolToUse(self):
        toolbox = Toolbox()
        self.assertEqual(0, self.human.toolsToUse(3, 2, toolbox))
        toolbox.upgrade()
        self.assertEqual(0, self.human.toolsToUse(3, 7, toolbox))
        toolbox.upgrade()
        self.assertEqual(0, self.human.toolsToUse(3, 9, toolbox))
        
    def testUseTools(self):
        toolbox = Toolbox()
        toolbox.upgrade()
        toolbox.upgrade()
        toolbox.upgrade()
        toolbox.upgrade()
        
        self.assertEquals([2,1,1], toolbox.getUnused())
        toolsToUse = [1]
        self.human.useTools(toolbox, toolsToUse)
        self.assertEquals([2,1], toolbox.getUnused())
    
    def testChooseChristmas(self):
        reducedList = self.player.chooseChristmas([3,4,7,9])
        self.assertTrue(set(reducedList).issubset(set([3,4,7,9])))
        self.assertEqual(3, len(reducedList))
    
#    def testHumanReeapingOrder(self):
#        self.player.chooseReapingResource ("fws")
        
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(HumanStrategyTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
