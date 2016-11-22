
'''

Euler's Totient function, φ(n) [sometimes called the phi function], is used to 
determine the number of numbers less than n which are relatively prime to n. 
For example, as 1, 2, 4, 5, 7, and 8, are all less than nine and relatively 
prime to nine, φ(9)=6. 

'''

from math import gcd

from utilities.divisors import getDivisors, getFactorization


def phi(n):
	return len([x for x in range(1, n) if gcd(x, n) == 1])		
		

if __name__ == '__main__':
	maxi = (2, 1)
	for n in range(2, 1000001):
		quot = n / phi(n)
		if quot > maxi[1]:
			maxi = (n, quot)
			print("% 8d" % n)
		
		
# 	print(max([(x / len(getFactorization(x)), x) for x in range(2, 1000001)]))
