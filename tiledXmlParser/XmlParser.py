'''
Created on Feb 5, 2015

@author: finn
'''
import xml.etree.ElementTree

class XmlParser:
    
    def __init__(self, tiledXmlFile):
        self.etree = xml.etree.ElementTree.parse(tiledXmlFile)
        self.root = self.etree.getroot()
        self.objectGroups = self.etree.findall("objectgroup")
    
    
    def getObjectGroupName(self):
        return self.objectGroups[0].attrib["name"]
    
    def getObjectGroupWidth(self):
        return int(self.objectGroups[0].attrib["width"])

    
    def getObjectGroupHeight(self):
        return int(self.objectGroups[0].attrib["height"])

    
    def getObjects(self, objectGroupName):
        target = [og for og in self.objectGroups if og.attrib["name"] == objectGroupName][0]
        return [Object(e) for e in target.findall("object")]

class Object:
    
    def __init__(self, element):
        self.element = element
    
    def getName(self):
        return self.element.attrib["name"]
    
    def getGid(self):
        return int(self.element.attrib["gid"])
    
    def getX(self):
        return int(self.element.attrib["x"])
    
    def getY(self):
        return int(self.element.attrib["y"])
    
    
    
    
    
    
    
    
    

