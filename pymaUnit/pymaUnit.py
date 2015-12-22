'''
Created on 22 Dec 2015
'''
class TestCase:
    def __init__(self, methodName):
        self.method = getattr(self, methodName)
        self.setUp()
        self.wasRun = False
        
    def run(self):
        self.method()
        
    def setUp(self):
        pass
        
class WasRun(TestCase):
    def doRun(self):
        self.wasRun = True
    
    def setUp(self):
        self.wasSetUp = True
        
    
class TestCaseTest(TestCase):
    def setUp(self):
        self.test = WasRun("doRun")
            
    def testSetUp(self):
        self.test.run()
        assert self.test.wasSetUp
    
    def testRunning(self):
        self.test.run()
        assert self.test.wasRun
    
if __name__ == '__main__':
    test = TestCaseTest("testSetUp")
    test.run()
    test = TestCaseTest("testRunning")
    test.run()


