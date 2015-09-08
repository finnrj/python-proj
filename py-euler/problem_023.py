'''
Created on Jun 2, 2015

'''
import string

def divisors(i):
    return [j for j in range(1, i // 2 + 1) if i % j == 0]

if __name__ == '__main__':
    abundantNumbers = [x for x in range(1, 28124) if sum(divisors(x)) > x]
    print(len(abundantNumbers), abundantNumbers)
