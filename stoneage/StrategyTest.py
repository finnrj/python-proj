'''
Created on Mar 30, 2013

@author: finn
'''
import unittest
from Strategy import Strategy, StrategyNotImplemented, Human
from Player import Player
from Board import Board
from Hut import SimpleHut, CountHut

class StrategyTest(unittest.TestCase):

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
        self.human.processPlacePersonsInput("f3", self.board)
        self.assertEqual(3, self.board.personsOnGrounds(self.human.player.getAbr()))

    def testHumanInputH5(self):
        self.human.processPlacePersonsInput("f5", self.board)
        self.assertEqual(5, self.board.personsOnGrounds(self.human.player.getAbr()))

#    Forest
    def testHumanInputF3(self):
        self.assertEqual(0, 7 - self.board.freeForestSlots())
        self.human.processPlacePersonsInput("w3", self.board)
        self.assertEqual(3, self.board.personsOnGrounds(self.human.player.getAbr()))
        self.assertEqual(3, 7 - self.board.freeForestSlots())
        
    def testHumanInputF5(self):
        self.assertEqual(0, 7 - self.board.freeForestSlots())
        self.human.processPlacePersonsInput("w5", self.board)
        self.assertEqual(5, self.board.personsOnGrounds(self.human.player.getAbr()))
        self.assertEqual(5, 7 - self.board.freeForestSlots())

    def testHumanInputBuilding2(self):
        self.assertEqual(4, len(self.board.availableHuts()))
        self.human.processPlacePersonsInput("h2", self.board)
        self.assertEqual(3, len(self.board.availableHuts()))
        
    def testProcessBuyHutInput(self):
        result = []
        hut = SimpleHut(3,3,3)
        self.player.addResources([3,3,3,4,5,5])
        self.human.processBuyHutInput(result, hut)
        self.assertIn(hut, result)

    def testHumanPaySimpleHut(self):
        self.player.addResources([3,3,4,4,5,5])
        self.assertEqual(12, self.human.pay(SimpleHut(3,4,5)))
        
    def testProcessPayHut(self):
        self.player.addResources([3,3,4,4,5,5])
        self.human.processPayHut("334")
        self.assertListEqual([4,5,5], self.player.getNonFood())
        
    def testProcessPayHutWithNoExistentResources(self):
        self.player.addResources([3,3,4,4,5,5])
        with self.assertRaises(ValueError):
            self.human.processPayHut("456")

    def testIllegalPaymentForCountHut(self):
        self.player.addResources([3,3,4,4,5,5])


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(StrategyTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
