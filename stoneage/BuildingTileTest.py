from BuildingTile import BuildingTile
import unittest

class BuildingTileTest(unittest.TestCase):
    pass

    # def testBuildingTileInitialization(self):
    #     hut = BuildingTile(  )

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(BuildingTileTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
# alternatively use this for shorter output
##    unittest.main()
