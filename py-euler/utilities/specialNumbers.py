'''
Created on Oct 7, 2015

@author: expert
'''

def isPandigital(n, numbers="123456789"):
    s = str(n)
    if len(s) != len(numbers):
        return False
    return all(c in s for c in numbers)

def generateFromLambda(f, count=10000):
    n = 1
    while n <= count:
        yield f(n)
        n += 1
        
if __name__ == '__main__':
    print(list(generateFromLambda(lambda n: n * (n + 1) // 2, 20)))
            
