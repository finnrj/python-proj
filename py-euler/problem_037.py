'''
The number 3797 has an interesting property. Being prime itself, it is possible to 
continuously remove digits from left to right, 
and remain prime at each stage: 3797, 797, 97, and 7. 
Similarly we can work from right to left: 3797, 379, 37, and 3.

Find the sum of the only eleven primes that are both truncatable from left to right 
and right to left.

NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.

'''

from utilities.divisors import isPrime, getPrimes

def hasProperty(p):
    return all(isPrime(i) for i in [int(p[i:]) for i in range(1, len(p))])\
        and all(isPrime(i) for i in [int(p[:-i]) for i in range(1, len(p))])

def ugly():
    for p in getPrimes():
        if hasProperty(str(p)):
            yield p

if __name__ == '__main__':
    print(hasProperty("3797"))
    result = [p for p in list(ugly())[4:15]]
    print(sum(result))
        