'''

The primes 3, 7, 109, and 673, are quite remarkable. By taking any two primes 
and concatenating them in any order the result will always be prime. For 
example, taking 7 and 109, both 7109 and 1097 are prime. The sum of these four 
primes, 792, represents the lowest sum for a set of four primes with this 
property. 

Find the lowest sum for a set of five primes for which any two primes 
concatenate to produce another prime. 



'''
from functools import lru_cache       
import itertools

from utilities import divisors
from utilities.divisors import isPrime


@lru_cache()
def allCombisArePrime(p1, p2):
	if(len(str(p1) + str(p2)) > 8):
		print(p1, p2)
		return False
	return isPrime(int(str(p1) + str(p2))) and isPrime(int(str(p2) + str(p1)))

def foursHasProperty(pair1, pair2):
	return allCombisArePrime(pair1[0], pair2[0]) and allCombisArePrime(pair1[0], pair2[1]) \
 			and allCombisArePrime(pair1[1], pair2[0]) and allCombisArePrime(pair1[1], pair2[1])

def nowDoIt():
	primes = divisors.allPrimesList[:1200]
	group1, group2 = [p for p in primes[1:] if p % 3 == 1 or p % 3 == 0], [p for p in primes[1:] if p % 3 == 2 or p % 3 == 0]
	group2.remove(5)
	for group in [group1, group2]:
		pairs = [p for p in itertools.combinations(group, 2) if allCombisArePrime(p[0], p[1])]
		print("finished pairs - pair size: ", len(pairs))
		fourth = set([tuple(sorted(p1 + p2)) for (p1, p2) in itertools.combinations(pairs, 2) if set(p1).isdisjoint(set(p2)) and foursHasProperty(p1, p2)])
		print("finished fourth", fourth)
		print(allCombisArePrime.cache_info())
		result = []
		for p in group:
			for f in fourth:
				if all([allCombisArePrime(p, i) for i in f]):
					result.append(f[:] + (p,))
		
		print("result:", sorted([sum(r) for r in result]))

if __name__ == '__main__':
# 195.4761392380001
	import timeit
	print(timeit.timeit('nowDoIt()', setup='from __main__ import nowDoIt', number=1))
	
