class ToolBox():
    """class representing the three tools for a player"""

    def __init__(self):
        self.tools = 3 * [0]
        
        
    def upgrade(self):
        self.tools[-1] += 1 
        self.tools = sorted(self.tools, reverse=True)
        
    def getTools(self):
        return self.tools[:]