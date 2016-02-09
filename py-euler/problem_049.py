'''

The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases 
by 3330, is unusual in two ways: (i) each of the three terms are prime, and, 
(ii) each of the 4-digit numbers are permutations of one another. 

There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, 
exhibiting this property, but there is one other 4-digit increasing sequence. 

What 12-digit number do you form by concatenating the three terms in this 
sequence? 

'''
from utilities.divisors import isPrime
from utilities.specialNumbers import isPermutation


def hasProperty(x):
	s = str(x)
	return isPermutation(x + 3330, s) and isPermutation(x + 2 * 3330, s) \
		and isPrime(x) and isPrime(x + 3330) and isPrime(x + 2 * 3330)

if __name__ == '__main__':
	print([str(i) + str(i + 3330) + str(i + 2 * 3330) for i in range(1487, 10000) if hasProperty(i)])
