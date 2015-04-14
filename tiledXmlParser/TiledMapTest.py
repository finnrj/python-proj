'''
Created on Feb 5, 2015

@author: finn & torsten
'''
import unittest
from TiledMap import TiledMap
from io import StringIO
import os
from pygame.surface import Surface

class Small_Map_tmx_Test(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.map = TiledMap(os.path.join("small_map"))
        
    def testObjectgroup(self):
        self.assertEqual(3, len(self.map.objectgroups))
        self.assertIsNotNone(self.map.objectgroups["background"])
        self.assertEqual(13, len(self.map.objectgroups["walls"]))
         
    def testObject(self):
        objects = self.map.objectgroups["walls"];
        o = objects[0]
        self.assertEqual(7, o.id)
        self.assertEqual(2, o.gid)
        self.assertEqual(0, o.x)
        self.assertEqual(320, o.y)
        
        o = objects[10]
        self.assertEqual(20, o.id)
        self.assertEqual(2, o.gid)
        self.assertEqual(96, o.x)
        self.assertEqual(224, o.y)
        
    def testImages(self):
        self.assertEquals(3, len(self.map.images))
        self.assertIs(type(self.map.images[2]), Surface)  # pygame.Surface?

if __name__ == "__main__":
    unittest.main()
    
