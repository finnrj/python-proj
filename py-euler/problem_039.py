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

def solutions3(p):
    return len([1 for a in range(p // 3) for b in range(a, (p - a) // 2) if a * b % 12 == 0 and isRightAngleTriangle(a, b, p)])

def solutions4(p):
    return len([1 for a in range(p // 3) for b in range(a, (p - a) // 2) if a * b % 12 == 0 and a * b * (p - a - b) % 60 == 0 and isRightAngleTriangle(a, b, p)])

if __name__ == '__main__':
    rounds = 3
    firstSolution = 'print(max([(solutions(p), p) for p in range(3, 1001)]))'
    print(timeit.timeit(firstSolution, setup='from __main__ import solutions', number=rounds) / rounds)
  
    secondSolution = 'print(max([(solutions2(p), p) for p in range(3, 1001)]))'
    print(timeit.timeit(secondSolution, setup='from __main__ import solutions2', number=rounds) / rounds)

    thirdSolution = 'print(max([(solutions3(p), p) for p in range(3, 1001)]))'
    print(timeit.timeit(thirdSolution, setup='from __main__ import solutions3', number=rounds) / rounds)

    fourthSolution = 'print(max([(solutions4(p), p) for p in range(3, 1001)]))'
    print(timeit.timeit(fourthSolution, setup='from __main__ import solutions4', number=rounds) / rounds)
    
