'''
Created on Feb 5, 2015

@author: finn
'''
import xml.etree.ElementTree
import pygame
import os

class TiledMap:
    
    def __init__(self, levelDir):
        assert os.path.exists(levelDir), "the dir of the map could not be found! Have dir and tmx-file the same name?"
        pathToTmxFile = os.path.join(levelDir, levelDir + ".tmx")
        assert os.path.exists(pathToTmxFile), "the tmx-file could not be found! Have dir and tmx-file the same name?"
        etree = xml.etree.ElementTree.parse(open(pathToTmxFile))
        
        self.objectgroups = dict((og.attrib["name"], [Object(o) for o in og.findall("object")]) for og in etree.findall("objectgroup"))
        self.images = self.createImageMap(levelDir, etree.findall("tileset"))
        
    def createImageMap(self, levelDir, tilesetElements):
        images = dict()
        for e in tilesetElements:
            pathToImage = os.path.join(levelDir, e.find("image").attrib["source"])
            assert os.path.exists(pathToImage), "image '" + pathToImage + "' not found!"
            images[int(e.attrib["firstgid"])] = pygame.image.load(pathToImage)
        
        return images
 
class Object:
    
    def __init__(self, element):
        self.id = int(element.attrib["id"])
        self.gid = int(element.attrib["gid"])
        self.x = int(element.attrib["x"])
        self.y = int(element.attrib["y"])
    
    
    
    
    
    
    
    
    

