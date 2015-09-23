'''
Created on Jun 2, 2015

 1001 * 1001 
'''
from math import sqrt

def tuesdayVersionCorrected():
    n = 121
    sqrtN = int(sqrt(n))
    f = [[0] * sqrtN for _ in range(sqrtN)]
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

def prettyPrint(f):
    offset = len((str(len(f) ** 2)))  # length of the biggest number
    
    for y in range(len(f)):
        for x in range(len(f)):
            i = str(f[x][y])
            print(" "*(offset - len(i)) + i, end=" ")
        print()
    print()
        
tupleAdd = lambda t1, t2 : (t1[0] + t2[0], t1[1] + t2[1])
right, left, up, down = (1, 0), (-1, 0), (0, -1), (0, 1)

def generateMoves(size):
    if size > 1:
        return [right]\
        + (size - 2) * [down]\
        + (size - 1) * [left]\
        + (size - 1) * [up]\
        + (size - 1) * [right]
    return [(0, 0)]

def wednesdayVersion(squareSize):
    f = [[0] * squareSize for _ in range(squareSize)]
    middle = squareSize // 2
    squareSizes = [n for n in range(1, squareSize + 1) if n % 2 == 1]

    nextNumber = 0
    x, y = (middle, middle)
    diagonalSum = 0
    for size in squareSizes:
        moves = generateMoves(size)
        for move in moves:
            nextNumber += 1
            x, y = tupleAdd((x, y), move)
            f[x][y] = nextNumber
            if x == y or x + y == squareSize - 1:
                diagonalSum += nextNumber 
    prettyPrint(f)
    print("diagonal sum: %d" % diagonalSum)

if __name__ == '__main__':
    tuesdayVersionCorrected()
    wednesdayVersion(11)
    

