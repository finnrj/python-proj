'''
Created on Oct 7, 2015

@author: expert
'''

def isPandigital(n, numbers="123456789"):
    s = str(n)
    if len(s) != len(numbers):
        return False
    return all(c in s for c in numbers)

def generatefromLambda(f, count=10000):
    n = 1
    while n <= count:
        yield f(n)
        n += 1
        
if __name__ == '__main__':
    print(list(generatefromLambda(lambda n: n * (n + 1) // 2, 20)))
            
# Pentagonal 
# Pn=n(3n−1)/2 
# 1, 5, 12, 22, 35, ... 
# 
# Hexagonal 
# Hn=n(2n−1) 
# 1, 6, 15, 28, 45, ... 
