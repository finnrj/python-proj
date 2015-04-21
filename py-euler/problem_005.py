'''
Created on Apr 21, 2015

@author: finn
'''

if __name__ == '__main__':
    n = 2520
    remainders = [1]
    while sum(remainders) != 0:
        n += 20
        remainders = [n % i for i in range(11, 21)]
    print("the ultimate solution: " , n)

