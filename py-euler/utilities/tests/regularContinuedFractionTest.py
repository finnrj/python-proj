import unittest
from fractions import Fraction
from utilities.RegularContinuedFraction import getRegularContinuedFraction,\
    regularContinuedFractionToFraction, getRepeatingRegContFrac

class Test(unittest.TestCase):


    def testgetRegularContinuedFraction73_29(self):
        f = Fraction(73,29)
        self.assertEqual([2, 1, 1, 14], getRegularContinuedFraction(f))
        
    def testgetRegularContinuedFraction1_15(self):
        f = Fraction(1,15)
        self.assertEqual([0, 15], getRegularContinuedFraction(f))
        
    def testRegularContinuedFractionToFraction1_15(self):
        self.assertEqual(Fraction(1,15), regularContinuedFractionToFraction([0, 15]))    
        
    def testRegularContinuedFractionToFraction73_29(self):
        self.assertEqual(Fraction(73,29), regularContinuedFractionToFraction([2, 1, 1, 14]))
        
    def testgetRepeatingRegContFrac(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()