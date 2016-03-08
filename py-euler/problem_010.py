'''
Created on Apr 21, 2015

@author: finn
'''


if __name__ == '__main__':
    hands = open("primes1.txt").readlines()[2:]
    print(sum([int(p) for l in hands for p in l.split() if int(p) < 2000000]))

          

            
    
    
