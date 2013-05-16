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

    def testUpgradesTo3(self):
        self.toolBox.upgrade()
        self.toolBox.upgrade()
        self.toolBox.upgrade()
        
        self.toolBox.upgrade()
        self.assertEqual([2, 1, 1], self.toolBox.getTools())
        self.toolBox.upgrade()
        self.toolBox.upgrade()
        self.assertEqual([2, 2, 2], self.toolBox.getTools())
        self.toolBox.upgrade()
        self.assertEqual([3, 2, 2], self.toolBox.getTools())

    def testUpgradesTo4(self):
        self.toolBox.upgrade()
        self.toolBox.upgrade()
        self.toolBox.upgrade()
        
        self.toolBox.upgrade()
        self.toolBox.upgrade()
        self.toolBox.upgrade()
        
        self.toolBox.upgrade()
        self.assertEqual([3, 2, 2], self.toolBox.getTools())
        self.toolBox.upgrade()
        self.toolBox.upgrade()
        self.assertEqual([3, 3, 3], self.toolBox.getTools())
        self.toolBox.upgrade()
        self.assertEqual([4, 3, 3], self.toolBox.getTools())

    def testNoUpgradesAbove4(self):
        self.toolBox.upgrade()
        self.toolBox.upgrade()
        self.toolBox.upgrade()
        
        self.toolBox.upgrade()
        self.toolBox.upgrade()
        self.toolBox.upgrade()
        
        self.toolBox.upgrade()
        self.toolBox.upgrade()
        self.toolBox.upgrade()
        
        self.toolBox.upgrade()
        self.toolBox.upgrade()
        self.toolBox.upgrade()
        self.assertEqual([4, 4, 4], self.toolBox.getTools())
        
        self.toolBox.upgrade()
        self.assertEqual([4, 4, 4], self.toolBox.getTools())
        self.toolBox.upgrade()
        self.assertEqual([4, 4, 4], self.toolBox.getTools())
        
        
    def testToolUsed(self):
        self.assertEqual([], self.toolBox.getUnused())
        self.toolBox.upgrade()
        self.assertEqual([1], self.toolBox.getUnused())
        self.toolBox.use(1)
        self.assertEqual([], self.toolBox.getUnused())
    

def main():
#    suite = unittest.TestLoader().loadTestsFromTestCase(BoardTest)
#    unittest.TextTestRunner(verbosity=2).run(suite)

    # alternatively use this for shorter output
    unittest.main()

if __name__ == '__main__':
    main()