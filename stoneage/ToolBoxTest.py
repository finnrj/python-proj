#! /usr/bin/env python3

import unittest
from ToolBox import ToolBox

class ToolBoxTest(unittest.TestCase):
    
    def setUp(self):
        self.toolBox = ToolBox()

    def testToolsAtStart(self):
        self.assertEqual([0, 0, 0], self.toolBox.getTools())

    def testUpgradesTo2(self):
        self.toolBox.upgrade()
        self.assertEqual([1, 0, 0], self.toolBox.getTools())
        self.toolBox.upgrade()
        self.assertEqual([1, 1, 0], self.toolBox.getTools())
        self.toolBox.upgrade()
        self.assertEqual([1, 1, 1], self.toolBox.getTools())
        self.toolBox.upgrade()
        self.assertEqual([2, 1, 1], self.toolBox.getTools())


def main():
#    suite = unittest.TestLoader().loadTestsFromTestCase(BoardTest)
#    unittest.TextTestRunner(verbosity=2).run(suite)

    # alternatively use this for shorter output
    unittest.main()

if __name__ == '__main__':
    main()