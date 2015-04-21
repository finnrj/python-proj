'''
Created on Apr 21, 2015

@author: finn
'''

if __name__ == '__main__':
    lines = open("primes1.txt").readlines()[2:]
    print([int(p) for l in lines for p in l.split()][10000])
