'''
Created on Apr 21, 2015

@author: finn
'''

if __name__ == '__main__':
    aRange = range(1, 101)
    print(sum([i for i in aRange]) ** 2 - sum([i ** 2 for i in aRange]))     
