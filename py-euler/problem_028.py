'''
Created on Jun 2, 2015

 1001 * 1001 
'''
from math import sqrt

def prettyPrint(f):
    offset = len((str(len(f) ** 2)))  # length of the biggest number
    
    for y in range(len(f)):
        for x in range(len(f)):
            i = str(f[x][y])
            print(" "*(offset - len(i)) + i, end=" ")
        
        print()
    
    print()
        
if __name__ == '__main__':
    n = 121
    sqrtN = int(sqrt(n))
    f = [[0] * sqrtN for x in range(sqrtN)]
    
    x = sqrtN // 2
    y = sqrtN // 2
    i = 1
    f[x][y] = i

    offset = 2
    while i < n:
        x += 1
        i += 1
        f[x][y] = i
        
        for _ in range(1, offset):
            y += 1
            i += 1
            f[x][y] = i
        for _ in range(1, offset + 1):
            x -= 1
            i += 1
            f[x][y] = i  
        for _ in range(1, offset + 1):
            y -= 1
            i += 1
            f[x][y] = i  
        for _ in range(1, offset + 1):
            x += 1
            i += 1
            f[x][y] = i  
            
        offset += 2

    prettyPrint(f)
