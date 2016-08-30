'''

The cube, 41063625 (345**3), can be permuted to produce two other cubes: 56623104 
(384**3) and 66430125 (405**3). In fact, 41063625 is the smallest cube which has 
exactly three permutations of its digits which are also cube. 

Find the smallest cube for which exactly five permutations of its digits are 
cube. 

'''
from utilities.specialNumbers import isPermutation

def getCandidate(start):
	n = start
	while len(str(n ** 3)) == len(str(start ** 3)):
		yield (n ** 3, n)
		n += 1

if __name__ == '__main__':
	print(10002 ** 3)
	for n in range(405, 100000):
		candidates = list(getCandidate(n))
		filteredCandidates = [c for c in candidates[1:] if isPermutation(c[0], str(candidates[0][0]))]
		if(len(filteredCandidates) == 4):
			print(candidates[0], filteredCandidates)
