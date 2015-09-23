'''
Created on Jun 2, 2015

 1001 * 1001 
'''
from math import sqrt

def tuesdayVersion():
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

def prettyPrint(f):
    for y in range(len(f)):
        for x in range(len(f)):
            print("% 5d" % f[x][y], end=" ")
        print()
        
if __name__ == '__main__':
#     tuesdayVersion()
    wednesdayVersion(5)
    

