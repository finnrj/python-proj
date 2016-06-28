'''

The primes 3, 7, 109, and 673, are quite remarkable. By taking any two primes 
and concatenating them in any order the result will always be prime. For 
example, taking 7 and 109, both 7109 and 1097 are prime. The sum of these four 
primes, 792, represents the lowest sum for a set of four primes with this 
property. 

Find the lowest sum for a set of five primes for which any two primes 
concatenate to produce another prime. 

'''
import itertools

from utilities import divisors
from utilities.divisors import isPrime

def allCombisArePrime(p1, p2):
	if(len(str(p1) + str(p2)) > 8):
		print(p1, p2)
		return False
	return isPrime(int(str(p1) + str(p2))) and isPrime(int(str(p2) + str(p1)))

def hasProperty(candidates):
	return all([allCombisArePrime(p1, p2) for p1, p2 in itertools.combinations(candidates, 2)])

def addPToSolutions(p, solutions):
	pass

def solve():
	solutionCandidates = [[3]]
	for p in divisors.allPrimesList[2:]:
		for s in solutionCandidates:
			for number in s:
				addPToSolutions(p, s)
					
	print("finished")				
			
				
		

if __name__ == '__main__':
# 	solve()
# 1000
	primes = divisors.allPrimesList[:1000]
	print(primes[-1])
	group1, group2 = [p for p in primes[1:] if p % 3 == 1 or p % 3 == 0], [p for p in primes[1:] if p % 3 == 2 or p % 3 == 0]
	group2.remove(5)
	print(len(group1), len(group2))
	
	for group in [group1, group2]:
		pairs = [p for p in itertools.combinations(group, 2) if hasProperty(p)]
		print("finished pairs - pair size: ", len(pairs))
		fourth = [p1 + p2 for p1, p2 in itertools.combinations(pairs, 2) if set(p1).isdisjoint(set(p2))
				and hasProperty(p1 + p2)]
		print("finished fourth")
# 		To evil
# 		threes = [p for p in itertools.combinations(group, 3) if hasProperty(p)]
# 		print("finished threes")
# 		for p in pairs:
# 			for t in threes:
# 				if set(p).isdisjoint(set(t)) and hasProperty(p + t):
# 					print(p + t)
# 		print("finished a group")
		
# 		print(len(fourth))
# # 		for p in divisors.allPrimesList:
# 		for p in group:
# 			for cand in fourth:
# 				if not p in cand and allCombisArePrime(cand[3], p) and allCombisArePrime(cand[2], p) and allCombisArePrime(cand[1], p) and allCombisArePrime(cand[0], p):
# 					candp = cand + [p]
# 					print(candp, sum(candp))
# 		print("finished a group")
# 	solution = max([sum(candidate) for candidate in itertools.combinations(group1, 5) if hasProperty(candidate)])
# 	print(solution)
