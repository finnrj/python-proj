'''
Created on Sep 16, 2015

@author: expert
'''
import unittest

from utilities.divisors import countDivisors
from utilities.divisors import getDivisors
from utilities.divisors import getFactorization


class Test(unittest.TestCase):
    
    def testGetFactorization50(self):
        factorization = getFactorization(50)
        for factor in [[2, 1], [3, 0], [5, 2]]:
            self.assertIn(factor, factorization)
            
    def testGetFactorizationOfToBigNumber(self):
        with self.assertRaises(Exception):
            getFactorization(15485867)  # 1.000.001th prime

            
    def testCountDivisors36(self):
        self.assertEqual(9, countDivisors(36))

    def testNoDoubleInGetDivisors36(self):
        divisors = getDivisors(36)
        self.assertEqual(len(divisors), len(set(divisors)))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
