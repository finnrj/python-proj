'''
Created on Apr 21, 2015

@author: finn
'''

if __name__ == '__main__':
    hands = open("utilities/primes.txt").readlines()[2:]
    print([int(p) for l in hands for p in l.split()][10000])
