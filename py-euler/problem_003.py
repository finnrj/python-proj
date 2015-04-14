'''
Created on Apr 14, 2015

'''

from math import sqrt

if __name__ == '__main__':
    lines = open("primes1.txt").readlines()[2:]
    prime_candidates = [int(p) for l in lines for p in l.split() if int(p) < sqrt(600851475143)]
    target = 600851475143
    
    print([p for p in prime_candidates if target % p == 0])
