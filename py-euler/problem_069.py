
'''

Euler's Totient function, φ(n) [sometimes called the phi function], is used to 
determine the number of numbers less than n which are relatively prime to n. 
For example, as 1, 2, 4, 5, 7, and 8, are all less than nine and relatively 
prime to nine, φ(9)=6. 

'''

from math import gcd
from timeit import Timer

from utilities.divisors import getDivisors, getFactorization


def phi_2(n):
	return len([x for x in range(1, n) if gcd(x, n) == 1])

def phi(n):
	result = n
	for p in getFactorization(n):
		result *= (1 - 1 / p[0])
	return result		
		
def find_solution(maxnumber, phi_func):
	maxi = (2, 1)
	for n in range(2, maxnumber):
		quot = n / phi_func(n)
		if quot > maxi[1]:
			maxi = (n, quot)
			print("% 8d" % maxi[0])
			
def time_some_phi_funcs():
	runs = 1
	t = Timer("find_solution(10000, phi)", "from __main__ import find_solution, phi")
	print("%.2f sec/pass" % (t.timeit(number=runs) / runs))
	t = Timer("find_solution(10000, phi_2)", "from __main__ import find_solution, phi_2")
	print("%.2f sec/pass" % (t.timeit(number=runs) / runs))

if __name__ == '__main__':
	find_solution(1000001, phi)
# 	time_some_phi_funcs()

# 	print(max([(x / len(getFactorization(x)), x) for x in range(2, 1000001)]))
