#! /usr/bin/env python3

from Hut import SimpleHut, AnyHut, CountHut
import unittest

class HutTest(unittest.TestCase):

    def testHutPayable(self):
        hut = SimpleHut(3,3,4)
        resources = [3,3,3,4,4]
                
        self.assertEqual([], hut.missing(resources))


    def testHutNotPayable(self):
        hut = SimpleHut(3,3,4)
        resources = [3,4,4,4]
                
        self.assertEqual([3], hut.missing(resources))


    def testHutNotPayable2(self):
        hut = SimpleHut(3,3,4)
        resources = [2,2,3,5,5]
                
        self.assertEqual([3,4], hut.missing(resources))

    def testAnyHutWithNoResources(self):
        hut = AnyHut()
        resources = []
        
        self.assertEqual([3], hut.missing(resources))
        
    def testAnyHutWithResources(self):
        hut = AnyHut()
        resources = [2,2,3,5,5]
        
        self.assertEqual([], hut.missing(resources))
        self.assertEqual([3,5,5], hut.costs(resources))

    def testAnyHutWithMoreThanSevenResources(self):
        hut = AnyHut()
        resources = [3,3,3,5,5,5,5,5]
        
        self.assertEqual([], hut.missing(resources))
        self.assertEqual([3,3,3,5,5,5,5], hut.costs(resources))


    def testAnyHutWithOnlyFood(self):
        hut = AnyHut()
        resources = [2,2]
        
        self.assertEqual([3], hut.missing(resources))
        self.assertEqual([], hut.costs(resources))
        
    def testCountHutWithNoResources(self):
        hut = CountHut(4,1)
        resources = []
        
        self.assertEqual([3,3,3,3], hut.missing(resources))
        
        hut = CountHut(4,3)
        resources = []
        self.assertListEqual([3,3,4,5], sorted(hut.missing(resources)))
        
        hut = CountHut(5,4)
        resources = []
        self.assertListEqual([3,3,4,5,6], sorted(hut.missing(resources)))

    def testCountHutWithEnoughResources(self):
        hut = CountHut(4,2)
        resources = [2,2,3,3,5,5,5]
        
        self.assertEqual([], hut.missing(resources))
        
        hut = CountHut(5,3)
        resources = [2,2,3,3,5,5,5,6]
        
        self.assertEqual([], hut.missing(resources))

        
        
    def testCountHutWithToFewResources(self):
        hut = CountHut(4,2)
        resources = [2,2,3,3,5]
        
        self.assertEqual([3], hut.missing(resources))
        
        hut = CountHut(4,4)
        resources = [2,2,3,3,5]
        
        self.assertEqual([4,6], hut.missing(resources))


        hut = CountHut(5,2)
        resources = [4,4,4,5]
        
        self.assertEqual([4], hut.missing(resources))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(HutTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
# alternatively use this for shorter output
##    unittest.main()
