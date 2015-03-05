'''
Created on Feb 5, 2015

@author: finn
'''
import unittest
from XmlParser import XmlParser
from io import StringIO
import os


class Test(unittest.TestCase):


    def testSingleObjectObjectGroup(self):
        xml = StringIO("""<map version="1.0" orientation="orthogonal" width="40" height="15" tilewidth="32" tileheight="32">
                                <objectgroup name="Objects" width="0" height="0">
                                      <object id="player" gid="14" x="27" y="416"/>
                                </objectgroup>
                          </map>""")
        
        self.parser = XmlParser(xml)
        objectGroup = self.parser.getGroupByName("Objects")
        self.assertEqual(0, objectGroup.getWidth())
        self.assertEqual(0, objectGroup.getHeight())
        
        objects = objectGroup.getObjects()
        self.assertIsNotNone(objects)
        self.assertEqual(1, len(objects))
        self.assertEqual("player", objects[0].getId())
        self.assertEqual(14, objects[0].getGid())
        self.assertEqual(27, objects[0].getX())
        self.assertEqual(416, objects[0].getY())
                
    def testMultipleObjectsObjectGroup(self):
        xml = StringIO("""<map version="1.0" orientation="orthogonal" width="40" height="15" tilewidth="32" tileheight="32">
                                <objectgroup name="Objects2" width="1" height="2">
                                      <object id="player" gid="14" x="27" y="416"/>
                                      <object id="hubba" gid="25" x="50" y="100"/>                              
                                </objectgroup>
                          </map>""")
        self.parser = XmlParser(xml)
        objectsGroups2 = self.parser.getGroupByName("Objects2")
        self.assertIsNotNone(objectsGroups2)
        self.assertEqual(1, objectsGroups2.getWidth())
        self.assertEqual(2, objectsGroups2.getHeight())
        objects = objectsGroups2.getObjects()
        self.assertIsNotNone(objects)
        self.assertEqual(2, len(objects))
        
        self.assertEqual("hubba", objects[1].getId())
        object1 = objectsGroups2.getObjectById("hubba")
        self.assertEqual(25, object1.getGid())
        self.assertEqual(50, object1.getX())
        self.assertEqual(100, object1.getY())
        
    def testSmallMap(self):
        self.parser = XmlParser(open("small_map/small_map.tmx"))
        self.assertEqual(3, len(self.parser.getObjectGroups()))
         
    def testSmallMapGroupName(self):
        self.parser = XmlParser(open("small_map/small_map.tmx"))
        wallsGroup = self.parser.getGroupByName("walls")
        self.assertIsNotNone(wallsGroup)
        
    def testTileset(self):
        self.parser = XmlParser(open("small_map/small_map.tmx"))
        self.assertEqual(3, len(self.parser.getTilesets()))
        evilStickman = self.parser.getTilesetByGid(3)
        self.assertEqual(3, evilStickman.getFirstgid())
        self.assertEqual(32, evilStickman.getTilewidth())
        self.assertEqual(64, evilStickman.getTileheight())



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    