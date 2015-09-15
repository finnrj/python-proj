'''
Created on Jun 2, 2015

'''
from math import sqrt
import string


def flatten(ts):
    return set(x for t in ts for x in t)

def divisors(x):
    return [1] + list(flatten([(x // n, n) for n in range(2, int(sqrt(x)) + 1) if x % n == 0]))

abundantNumbers = [x for x in range(1, 28124) if sum(divisors(x)) > x]

def sumOfPair(n):
    for abundandNumber in abundantNumbers:
        if n - abundandNumber in abundantNumbers:
            return True
    return False

if __name__ == '__main__':
    print(len(abundantNumbers), abundantNumbers)
    allNumbers = [i for i in range(1, 28124) if not sumOfPair(i)]
    print(sum(allNumbers))
    
