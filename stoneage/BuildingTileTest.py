#! /usr/bin/env python3

from BuildingTile import BuildingTile
import unittest

class BuildingTileTest(unittest.TestCase):

    def testBuildingTilePayable(self):
        hut = BuildingTile(3,3,4)
        resources = [3,3,3,4,4]
                
        self.assertEquals([], hut.missing(resources))


    def testBuildingTileNotPayable(self):
        hut = BuildingTile(3,3,4)
        resources = [3,4,4,4]
                
        self.assertEquals([3], hut.missing(resources))


    def testBuildingTileNotPayable2(self):
        hut = BuildingTile(3,3,4)
        resources = [2,2,3,5,5]
                
        self.assertEquals([3,4], hut.missing(resources))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(BuildingTileTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
# alternatively use this for shorter output
##    unittest.main()
