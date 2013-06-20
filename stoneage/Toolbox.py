class Toolbox():
    """class representing the three tools for a player"""

    def __init__(self):
        self.tools = 3 * [0]
        self.used = 3 * [False]

    def reset(self):
        self.used = 3 * [False]
        
    def upgrade(self):
        if sum(self.tools) >= 12: return
        self.tools[-1] += 1
        self.rotate()

    def rotate(self):
        self.tools = self.tools[2:] + self.tools[:2]
        self.used = self.used[2:] + self.used[:2]
         
    def getTools(self):
        return self.tools[:]
    
    def getUnused(self):
        """returns list of unused tool values"""
        return [tool for (tool, isUsed) in zip(self.tools, self.used) if not isUsed and tool != 0]

    def getUsed(self):
        """returns list of used tool values"""
        return [tool for (tool, isUsed) in zip(self.tools, self.used) if isUsed and tool != 0]

    def use(self, value):
        for index, (tool, isUsed) in enumerate(zip(self.tools, self.used)):
            if tool == value and not isUsed:
                self.used[index] = True
                return
        raise ToolError("No unused tool of value %d" % value)
    
    def __str__(self):
        return "%s used: %s" % (str(self.getUnused()), str(self.getUsed())) 
    
class ToolError(Exception):
    """Exception class for unavailable tool value"""
    def __init__(self, msg):
        Exception.__init__(self, msg)
    
    
    
