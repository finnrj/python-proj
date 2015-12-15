'''

We shall say that an n-digit number is pandigital if it makes use of all the 
digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital and is 
also prime. 

What is the largest n-digit pandigital prime that exists? 

'''
from itertools import permutations
from string import digits

from utilities.divisors import isPrime


if __name__ == '__main__':
	for to in range(9, 1, -1):
		candidates = ([int("".join(p)) for p in list(permutations([i for i in digits[1:to]]))
				if isPrime(int("".join(p)))])
		print(max(candidates) if candidates else "empty")
