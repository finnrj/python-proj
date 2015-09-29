'''

'''

from _functools import reduce
from fractions import Fraction

def isTarget(a, b):
    fraction = float(a) / float(b)
    if fraction >= 1:
        return False
    
    for c in a:
        if c in b:
            return c != "0" and float(a.replace(c, "", 1)) / float(b.replace(c, "", 1)) == fraction
        
    return False

if __name__ == '__main__':
    targets = [(a, b) for b in range(11, 100) for a in range(10, b) if a % 10 != 0 and b % 10 != 0 and isTarget(str(a), str(b))]
    print(targets)
    n, d = reduce(lambda t1, t2: (t1[0] * t2[0], t1[1] * t2[1]), targets, (1, 1))
    print(Fraction(n, d))