'''


145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.

Find the sum of all numbers which are equal to the sum of the factorial of their digits.

Note: as 1! = 1 and 2! = 2 are not sums they are not included.





'''
from math import factorial
from time import localtime
import time


def getExponent():
    n = 1
    while (n * factorial(9) > 10 ** n):
        n += 1
    return n

def isCurious(n):
    originalN = n
    s = 0
    while n > 0:
#         print(divmod(n, 10))
        n, m = divmod(n, 10) 
        s += factorial(m)
    return s == originalN
    
def isCurious2(n):
    return sum([factorial(int(s)) for s in str(n)]) == n


if __name__ == '__main__':
    start = time.time()
    print(sum([x for x in range(10, 10 ** getExponent()) if isCurious(x)]))
    print(time.time() - start)
     
    start = time.time()
    print(sum([x for x in range(10, 10 ** getExponent()) if isCurious2(x)]))
    print(time.time() - start)
