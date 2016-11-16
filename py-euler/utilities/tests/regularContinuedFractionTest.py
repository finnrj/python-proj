from fractions import Fraction
import unittest

from utilities.RegularContinuedFraction import getRegularContinuedFraction, \
    regularContinuedFractionToFraction, getRepeatingRegContFrac


class Test(unittest.TestCase):


    def testgetRegularContinuedFraction73_29(self):
        f = Fraction(73, 29)
        self.assertEqual([2, 1, 1, 14], getRegularContinuedFraction(f))
        
    def testgetRegularContinuedFraction1_15(self):
        f = Fraction(1, 15)
        self.assertEqual([0, 15], getRegularContinuedFraction(f))
        
    def testRegularContinuedFractionToFraction1_15(self):
        self.assertEqual(Fraction(1, 15), regularContinuedFractionToFraction([0, 15]))    
        
    def testRegularContinuedFractionToFraction73_29(self):
        self.assertEqual(Fraction(73, 29), regularContinuedFractionToFraction([2, 1, 1, 14]))
    
    def testGetRepeatingRegContFrac2(self):
        self.assertEqual([1, 2], getRepeatingRegContFrac(2))
    
    def testGetRepeatingRegContFrac7(self):
        self.assertEqual([2, 1, 1, 1, 4], getRepeatingRegContFrac(7))
        
    def testGetRepeatingRegContFrac3(self):
        self.assertEqual([1, 1, 2], getRepeatingRegContFrac(3))

    def testGetRepeatingRegContFrac13(self):
        self.assertEqual([3, 1, 2, 1, 6], getRepeatingRegContFrac(14))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
