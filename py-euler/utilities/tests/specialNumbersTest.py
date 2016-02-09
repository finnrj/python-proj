'''
Created on Jan 20, 2016

@author: expert
'''
import unittest
from utilities.specialNumbers import generateFromLambda, isPermutation


class Test(unittest.TestCase):

    def testGenerateFromLambdaTriangle(self):
        self.assertEqual(21, list(generateFromLambda(lambda n: n * (n + 1) // 2, 20))[5])

    def testGenerateFromLambdaPentagonal(self):
        self.assertEqual(22, list(generateFromLambda(lambda n: n * (3 * n - 1) // 2, 20))[3])

    def testIsPandigital(self):
        self.assertEqual(True, isPermutation(734289165), "with default value 123456789")
        self.assertEqual(False, isPermutation(73489165), "with default value 123456789")
        self.assertEqual(False, isPermutation(774289165), "with default value 123456789")
        
        self.assertEqual(True, isPermutation(123, "123"))
        self.assertEqual(False, isPermutation(13, "123"))
        self.assertEqual(False, isPermutation(13, ""))
        
        self.assertEqual(False, isPermutation(133, "123"))
        self.assertEqual(False, isPermutation(123, "122"))
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
