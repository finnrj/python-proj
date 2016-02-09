'''

The prime 41, can be written as the sum of six consecutive primes: 

41 = 2 + 3 + 5 + 7 + 11 + 13 

This is the longest sum of consecutive primes that adds to a prime below one-hundred.

The longest sum of consecutive primes below one-thousand that adds to a prime, contains 21 terms, and is equal to 953.

Which prime, below one-million, can be written as the sum of the most consecutive primes?
'''
from utilities.divisors import getPrimes, isPrime

def consecutivePrimesFrom(primes, start, maxvalue):
	result = []
	for i in range(start + 1, len(primes)):
		partsum = sum(primes[start:i + 1])
		if(isPrime(partsum) and partsum < maxvalue):
			result.append(primes[start:i + 1])
		if(partsum > maxvalue):
			return result
	
	return result


if __name__ == '__main__':
	maxvalue = pow(10, 6)
	primes = getPrimes(maxvalue)
	candidates = [consecutivePrimesFrom(primes, i, maxvalue)[-1] for i in range(maxvalue) if len(consecutivePrimesFrom(primes, i, maxvalue)) > 0]
	maxi = max(candidates, key=lambda l:len(l))
	print(sum(maxi), maxi)
	
