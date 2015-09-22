'''
Created on Jun 2, 2015

 1001 * 1001 
'''
from math import sqrt

def prettyPrint(f):
    for y in range(len(f)):
        for x in range(len(f)):
            print(f[x][y], end=" ")
        print()
        
if __name__ == '__main__':
    n = 49
    sqrtN = int(sqrt(n))
    f = [[0] * sqrtN for x in range(sqrtN)]
    print(f)
    
    i = 1
    xMiddle = sqrtN // 2
    yMiddle = sqrtN // 2
    f[xMiddle][yMiddle] = i
    
    i = 9
    x = xMiddle + 1
    y = yMiddle - 1
    offset = 4
    
    while i < n:
        prettyPrint(f)
        x += 1
        i += 1
        print(i)
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
