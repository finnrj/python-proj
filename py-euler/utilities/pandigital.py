'''
Created on Oct 7, 2015

@author: expert
'''

def isPandigital(n, numbers="123456789"):
    s = str(n)
    if len(s) != len(numbers):
        return False
    return all(c in s for c in numbers)