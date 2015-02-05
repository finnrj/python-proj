'''
Created on Feb 5, 2015

@author: finn
'''
import unittest
from XmlParser import XmlParser
from io import StringIO


class Test(unittest.TestCase):


    def testSingleObjectObjectGroup(self):
        xml = StringIO("""<map version="1.0" orientation="orthogonal" width="40" height="15" tilewidth="32" tileheight="32">
                                <objectgroup name="Objects" width="0" height="0">
                                      <object name="player" gid="14" x="27" y="416"/>
                                </objectgroup>
                          </map>""")
        
        self.parser = XmlParser(xml)
        self.assertEqual("Objects", self.parser.getObjectGroupName())
        self.assertEqual(0, self.parser.getObjectGroupWidth())
        self.assertEqual(0, self.parser.getObjectGroupHeight())
        self.assertIsNotNone(self.parser.getObjects("Objects"))
        self.assertEqual(1, len(self.parser.getObjects("Objects")))
        self.assertEqual("player", self.parser.getObjects("Objects")[0].getName())
        self.assertEqual(14, self.parser.getObjects("Objects")[0].getGid())
        self.assertEqual(27, self.parser.getObjects("Objects")[0].getX())
        self.assertEqual(416, self.parser.getObjects("Objects")[0].getY())
                
    def testMultipleObjectsObjectGroup(self):
        xml = StringIO("""<map version="1.0" orientation="orthogonal" width="40" height="15" tilewidth="32" tileheight="32">
                                <objectgroup name="Objects2" width="1" height="2">
                                      <object name="player" gid="14" x="27" y="416"/>
                                      <object name="hubba" gid="25" x="50" y="100"/>                              
                                </objectgroup>
                          </map>""")
        self.parser = XmlParser(xml)
        self.assertEqual("Objects2", self.parser.getObjectGroupName())
        self.assertEqual(1, self.parser.getObjectGroupWidth())
        self.assertEqual(2, self.parser.getObjectGroupHeight())
        self.assertIsNotNone(self.parser.getObjects("Objects2"))
        self.assertEqual(2, len(self.parser.getObjects("Objects2")))
        self.assertEqual("hubba", self.parser.getObjects("Objects2")[1].getName())
        self.assertEqual(25, self.parser.getObjects("Objects2")[1].getGid())
        self.assertEqual(50, self.parser.getObjects("Objects2")[1].getX())
        self.assertEqual(100, self.parser.getObjects("Objects2")[1].getY())
    

        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()