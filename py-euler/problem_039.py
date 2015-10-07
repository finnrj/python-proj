'''
f p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, 
here are exactly three solutions for p = 120.

{20,48,52}, {24,45,51}, {30,40,50}

For which value of p ≤ 1000, is the number of solutions maximised?
'''

def isRightAngleTriangle(a, b, p):
    c = p - a - b
    return a ** 2 + b ** 2 == c ** 2

def solutions(p):
    return len([1 for a in range(p // 3) for b in range(a, p // 2) if isRightAngleTriangle(a, b, p)])


if __name__ == '__main__':
    print(max([(solutions(p), p) for p in range(3, 1001)]))
