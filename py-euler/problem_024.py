'''
Created on Jun 2, 2015

'''
from itertools import permutations

if __name__ == '__main__':
    print("".join([str(d) for d in list(permutations([i for i in range(10)]))[999999]]))
