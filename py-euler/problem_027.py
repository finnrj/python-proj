'''
Created on Jun 2, 2015


 n² + an + b = prime, where |a| < 1000 and |b| < 1000
 
 b is prime 
'''
from utilities.divisors import getPrimes, isPrime

if __name__ == '__main__':
    maximum = (1, 1, 1)
    
    for b in getPrimes(1000):
        for a in range(-999, 1000, 2):
            res = b
            n = 0
            while isPrime(res):
                n += 1
                res = n ** 2 + a * n + b
            if(maximum[-1] < n):
                print("scooby doo ", maximum[-1], n)
                maximum = (a, b, n)
            print(a, b, n)
    print(maximum) 
    print(maximum[0] * maximum[1])
