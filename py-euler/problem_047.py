'''

The first two consecutive numbers to have two distinct prime factors are: 
14 = 2 × 7 and 15 = 3 × 5 

The first three consecutive numbers to have three distinct prime factors are: 
644 = 2² × 7 × 23 and 645 = 3 × 5 × 43 and 646 = 2 × 17 × 19. 

Find the first four consecutive integers to have four distinct prime factors. 
What is the first of these numbers? 
'''
from utilities.divisors import getFactorization

if __name__ == '__main__':
	facs = {}
	for i in range(125125, 1000000):
		facs.setdefault(i, getFactorization(i))
		if len(facs[i]) == 4:
			print(i, facs[i])
		for n in range(i, i + 4):
			facs.setdefault(n, getFactorization(n))
		if(all([len(facs[n]) == 4 for n in range(i, i + 4)])):
			print("solution: %d" % i)
			break
		
			
# 	print([i for i in range(1000000) if all([len(getFactorization(n)) == 4 for n in range(i, i + 4)])])
# 	print(getFactorization(644))
