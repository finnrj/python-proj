'''

By replacing the 1st digit of the 2-digit number *3, it turns out that six of 
the nine possible values: 13, 23, 43, 53, 73, and 83, are all prime. 

By replacing the 3rd and 4th digits of 56**3 with the same digit, this 5-digit 
number is the first example having seven primes among the ten generated 
numbers, yielding the family: 56003, 56113, 56333, 56443, 56663, 56773, and 
56993. Consequently 56003, being the first member of this family, is the 
smallest prime with this property. 

Find the smallest prime which, by replacing part of the number (not necessarily 
adjacent digits) with the same digit, is part of an eight prime value family. 

'''
from itertools import combinations
import string

from utilities.divisors import getPrimes, isPrime


def hasAsLeastNSameDigits(x, n):
	for i in range(0, 10):
		if str(x).count(str(i)) >= n:
			return True
	return False

def getCandidates(lengthOfCandidates, n):
	primes = getPrimes(int("9"*lengthOfCandidates))
	return [i for i in primes if len(str(i)) == lengthOfCandidates and hasAsLeastNSameDigits(i, n)]

def getPossiblePos(p, replacements):
	result = []
	sp = str(p)
	for ch in set(sp):
		if sp.count(ch) >= 3:
			start = 0
			r = []
			while sp.find(ch, start, len(sp)) >= 0:
				foundIndex = sp.find(ch, start, len(sp))
				r.append(foundIndex)
				start = foundIndex + 1
			result.extend(list(combinations(r, replacements))) 	
	return result

def rep(s, t, i):
	r = s[:]
	for j in t:
		r = r[:j] + i + r[j + 1:]
	return r

def hasProperty(candidate, targetNumber, digitCount):
	for t in candidate[1]:
		result = []
		for i in string.digits:
			pc = int(rep(candidate[0], t, i))
			if isPrime(pc) and len(str(pc)) == digitCount:
				result.append(int(rep(candidate[0], t, i)))
		if(len(result) >= targetNumber):
			print(result)
			return True
		
	return False
	
if __name__ == '__main__':
	replacements = 3
	digitCount = 6 
	candidates = getCandidates(digitCount, replacements)
	l = [(str(p), getPossiblePos(p, replacements)) for p in candidates]
	print(sorted([p for p in l if hasProperty(p, 8, digitCount)]))
