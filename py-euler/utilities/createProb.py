'''
Created on Oct 20, 2015

@author: expert
'''

from html.parser import HTMLParser
import os.path
import urllib.request


baseProblemSite = "https://projecteuler.net/problem="
targetProblems = range(60, 69)

class EulerProblemHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        
        self.inProbSection = False
        self.probDescription = ""
    
    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for key, value in attrs:
                if key == "class" and value == "problem_content":
                    self.inProbSection = True
                    
    def handle_endtag(self, tag):
        if tag == "div":
            self.inProbSection = False
            
    def handle_data(self, data):
        if self.inProbSection:
            self.probDescription += data
            

    def shortenLines(self, hands, maxLineLength=80):
        result = []
        for line in hands:
            lineLength = 0
            shortenedLine = ""
            words = line.split(" ")
            
            for word in words:
                lineLength += len(word) + 1
                if lineLength > maxLineLength:
                    shortenedLine += "\n"
                    lineLength = len(word) + 1
                shortenedLine += word + " "
                
            result.append(shortenedLine)
            
        return result

    def getFormatedProbDescription(self):
        return "\n\n".join(self.shortenLines(self.probDescription.strip().split("\n")))


def createProblem(target):
    filePath = "../problem_" + "0"*(3 - len(target)) + target + ".py"
    if os.path.isfile(filePath):
        print("'" + filePath + "' already exists!")
        return
        
    with urllib.request.urlopen(baseProblemSite + target) as response: 
        parser = EulerProblemHTMLParser()
        parser.feed(str(response.read(), encoding='utf-8'))               
        
        file = open(filePath, "w")
        file.write("'''\n\n"
                   + parser.getFormatedProbDescription()
                   + "\n\n'''"
                   + "\n\nif __name__ == '__main__':"
                   + "\n\tpass")
        
        
if __name__ == '__main__':
    for target in targetProblems:
        createProblem(str(target))
    

