'''
Created on Jan 20, 2016

@author: expert
'''
import unittest
import utilities.divisors as divisors
from utilities.divisors import isPrime, getPrimes, getFactorization, getDivisors, \
    countDivisors


class Test(unittest.TestCase):

    def testIsPrime(self):
        self.assertEqual(False, isPrime(4))
        self.assertEqual(True, isPrime(2))
        self.assertEqual(False, isPrime(1))
        self.assertEqual(False, isPrime(0))
        
        self.assertRaises(Exception, isPrime, divisors.biggestPrime + 1)
        
    def testGetPrimes(self):
        self.assertEqual([], getPrimes(0))
        self.assertEqual([2, 3, 5, 7], getPrimes(7))
        
        self.assertRaises(Exception, getPrimes, divisors.biggestPrime + 1)
        
    def testGetFactorization(self):
        self.assertEqual([], getFactorization(1))
        self.assertEqual([[2, 1]], getFactorization(2))
        self.assertEqual([[2, 1], [5, 2]], getFactorization(50))
        
        self.assertRaises(AssertionError, getFactorization, 0)
        self.assertRaises(AssertionError, getFactorization, 0.5)
        
    def testGetDivisors(self):
        self.assertEqual([1, 2, 4, 5, 10, 20], getDivisors(20))
        
    def testNoDoublesInGetDivisors(self):
        divisors = getDivisors(36)
        self.assertEqual(len(divisors), len(set(divisors)))
        
    def testCountDivisors(self):
        self.assertEqual(6, countDivisors(20))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testIsPrime']
    unittest.main()
