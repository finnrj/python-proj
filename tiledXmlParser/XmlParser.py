'''
Created on Feb 5, 2015

@author: finn
'''
import xml.etree.ElementTree

class XmlParser:
    
    def __init__(self, tiledXmlFile):
        self.etree = xml.etree.ElementTree.parse(tiledXmlFile)
        self.root = self.etree.getroot()
        self.xmlObjectGroups = self.etree.findall("objectgroup")
        self.tilesets = self.etree.findall("tileset")

    def getObjectGroups(self):
        return self.xmlObjectGroups
    
    def getGroupByName(self, objectGroupName):
        return ObjectGroup([og for og in self.xmlObjectGroups if og.attrib["name"] == objectGroupName][0])
    
    def getTilesets(self):
        return self.tilesets

    
    def getTilesetByGid(self, gid):
        xmlTilesets = self.etree.findall("tileset")
        return Tileset([t for t in xmlTilesets if t.attrib["firstgid"] == str(gid)][0])
    
class Tileset:
    def __init__(self, element):    
        self.element = element
        
    def getFirstgid(self):
        return int(self.element.attrib["firstgid"])
    
    def getTilewidth(self):
        return int(self.element.attrib["tilewidth"])
    
    def getTileheight(self):
        return int(self.element.attrib["tileheight"])
    
    def getName(self):
        return self.element.attrib["name"]
    
class ObjectGroup:
    def __init__(self, element):
        self.element = element
        self.objects = [Object(e) for e in element.findall("object")]
        self.osmap = dict((o.getId(), o) for o in self.objects)

    def getWidth(self):
        return int(self.element.attrib["width"])

    def getHeight(self):
        return int(self.element.attrib["height"])
    
    def getObjects(self):
        return self.objects
    
    def getObjectById(self, name):
        return [o for o in self.objects if o.getId() == name][0]

class Object:
    
    def __init__(self, element):
        self.element = element
    
    def getId(self):
        return self.element.attrib["id"]
    
    def getGid(self):
        return int(self.element.attrib["gid"])
    
    def getX(self):
        return int(self.element.attrib["x"])
    
    def getY(self):
        return int(self.element.attrib["y"])
    
    
    
    
    
    
    
    
    

