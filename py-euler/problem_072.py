'''

Consider the fraction, primes/d, where primes and d are positive integers. If nd and 
HCF(primes,d)=1, it is called a reduced proper fraction. 

If we list the set of reduced proper fractions for d ≤ 8 in ascending order of 
size, we get: 

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 
3/4, 4/5, 5/6, 6/7, 7/8 

It can be seen that there are 21 elements in this set. 

How many elements would be contained in the set of reduced proper fractions for 
d ≤ 1,000,000? 

'''
from fractions import Fraction
from utilities.divisors import getFactorization, isPrime


def phi(n):
	result = n
	if isPrime(n):
		return n - 1
	for p in getFactorization(n):
		result *= (1 - 1 / p[0])
	return result	

def find_solution(maxi):
	return sum(phi(n) for n in range(2, maxi))
	
if __name__ == '__main__':
# 	maxi = 10 ** 6
# 	print(sum(phi(n) for n in range(2, maxi)))
	
	import cProfile
	cProfile.run('find_solution(10**5)')	

