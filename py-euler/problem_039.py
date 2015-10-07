'''
f p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, 
here are exactly three solutions for p = 120.

{20,48,52}, {24,45,51}, {30,40,50}

For which value of p ≤ 1000, is the number of solutions maximised?
'''
import timeit

def isRightAngleTriangle(a, b, p):
    c = p - a - b
    return a ** 2 + b ** 2 == c ** 2

def solutions(p):
    return len([1 for a in range(p // 3) for b in range(a, p // 2) if isRightAngleTriangle(a, b, p)])

def solutions2(p):
    return len([1 for a in range(p // 3) for b in range(a, p // 2) if a * b % 12 == 0 and isRightAngleTriangle(a, b, p)])

if __name__ == '__main__':
    firstSolution = 'print(max([(solutions(p), p) for p in range(3, 1001)]))'
    print(timeit.timeit(firstSolution, setup='from __main__ import solutions', number=3))

    secondSolution = 'print(max([(solutions2(p), p) for p in range(3, 1001)]))'
    print(timeit.timeit(secondSolution, setup='from __main__ import solutions2', number=3))
    
