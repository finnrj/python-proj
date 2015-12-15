'''

An irrational decimal fraction is created by concatenating the positive integers:

0.123456789101112131415161718192021...

It can be seen that the 12th digit of the fractional part is 1.

If dn represents the nth digit of the fractional part, find the value of the following expression.

d1 × d10 × d100 × d1000 × d10000 × d100000 × d1000000

'''

from _functools import reduce
from _operator import mul
from math import log10


if __name__ == '__main__':
    upperBound = 1000000
    n = "".join([str(i) for i in range(upperBound)])
    targets = [int(n[10 ** i]) for i in range(int(log10(upperBound)) + 1)]       
    print(reduce(mul, targets))
