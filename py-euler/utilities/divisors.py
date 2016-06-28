'''
Created on Sep 10, 2015

@author: expert
'''

from _functools import reduce
from itertools import product
from operator import mul
import os.path

lastPrimeFileNotParsed = 1
primeFolder = "primes"

pathToPrimesFile = os.path.join(os.path.dirname(__file__), primeFolder + "/primes.txt")  # contains first 1.000.000 primes
assert os.path.isfile(pathToPrimesFile), pathToPrimesFile + " does not exist!"
with open(pathToPrimesFile) as fil:
    allPrimesList = list([int(p) for line in fil.readlines()[2:-1:2] for p in line.split()])
    biggestPrime = allPrimesList[-1]
    allPrimes = set(allPrimesList)
    
def parseNewPrimes():
    global lastPrimeFileNotParsed, biggestPrime, allPrimesList, allPrimes
    lastPrimeFileNotParsed += 1
    pathToPrimesFile = os.path.join(os.path.dirname(__file__), primeFolder + "/primes" + str(lastPrimeFileNotParsed) + ".txt")
    assert os.path.isfile(pathToPrimesFile), pathToPrimesFile + " does not exist!"
    with open(pathToPrimesFile) as fil:
        newPrimesAsList = [int(p) for line in fil.readlines()[2:] for p in line.split() if line]
        allPrimesList.extend(newPrimesAsList)
        biggestPrime = allPrimesList[-1]
        allPrimes.update(set(newPrimesAsList))
    
def getFactorization(x):
    """ Returns a list which represents factorization of x:
        The "tuples" in the list have the form [prime, powerOfPrime].
        For Example getFactorization(50) returns [[2, 1], [5, 2]] = 2^1 * 5^2 = 50
    """
    assert isinstance(x, int) and x > 0, "Factorization is only defined for integer numbers greater than 0"
    
    result = []
    for prime in allPrimesList:  # it is imported that the primes are ordered according to their size
        power = 0
        while x % prime == 0:
            power += 1
            x = x / prime
        if(power > 0):
            result.append([prime, power])
        
        if x == 1: return result
            
    raise Exception("not enough primes in " + pathToPrimesFile + " for factorization of " + str(x))

def countDivisors(x):
    return reduce(mul, [factor[1] + 1 for factor in getFactorization(x)], 1)

def getDivisors(x):
    result = [1]
    for factor in getFactorization(x):
        divisorsOfFactor = [factor[0] ** i for i in range(1, factor[1] + 1)]
        result += [a * b for a, b in list(product(result, divisorsOfFactor))]
    
    return result  

def getPrimes(maximum=15485863):
    if(maximum > biggestPrime):
        raise Exception("maximum is bigger than the biggest prime in " + pathToPrimesFile)
    
    return [p for p in allPrimes if p <= maximum]

def isPrime(candidate):
    while(candidate > biggestPrime):
        print("parsing next 1.000.000 primes (from 'primes" + str(lastPrimeFileNotParsed + 1) + ".txt')")
        parseNewPrimes()
    
    return candidate in allPrimes

