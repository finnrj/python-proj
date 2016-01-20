'''
Created on Jan 20, 2016

@author: expert
'''
import unittest
from utilities.specialNumbers import generateFromLambda, isPandigital


class Test(unittest.TestCase):

    def testGenerateFromLambdaTriangle(self):
        self.assertEqual(21, list(generateFromLambda(lambda n: n * (n + 1) // 2, 20))[5])

    def testGenerateFromLambdaPentagonal(self):
        self.assertEqual(22, list(generateFromLambda(lambda n: n * (3 * n - 1) // 2, 20))[3])

    def testIsPandigital(self):
        self.assertEqual(True, isPandigital(734289165), "with default value 123456789")
        self.assertEqual(False, isPandigital(73489165), "with default value 123456789")
        self.assertEqual(False, isPandigital(774289165), "with default value 123456789")
        
        self.assertEqual(True, isPandigital(123, "123"))
        self.assertEqual(False, isPandigital(13, "123"))
        self.assertEqual(False, isPandigital(13, ""))
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
