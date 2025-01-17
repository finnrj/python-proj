'''

Triangle, square, pentagonal, hexagonal, heptagonal, and octagonal numbers are 
all figurate (polygonal) numbers and are generated by the following formulae: 

Triangle 	  	P3,n=n(n+1)/2 	  	1, 3, 6, 10, 15, ...
Square 	  	    P4,n=n2 	  	    1, 4, 9, 16, 25, ...
Pentagonal 	  	P5,n=n(3n−1)/2 	  	1, 5, 12, 22, 35, ...
Hexagonal 	  	P6,n=n(2n−1) 	  	1, 6, 15, 28, 45, ...
Heptagonal 	  	P7,n=n(5n−3)/2 	  	1, 7, 18, 34, 55, ...
Octagonal 	  	P8,n=n(3n−2) 	  	1, 8, 21, 40, 65, ...
The ordered set of three 4-digit numbers: 8128, 2882, 8281, has three 
interesting properties. 

The set is cyclic, in that the last two digits of each number is the first two 
digits of the next number (including the last number with the first). 

Each polygonal type: triangle (P3,127=8128), square (P4,91=8281), and 
pentagonal (P5,44=2882), is represented by a different number in the set. 

This is the only set of 4-digit numbers with this property. 

Find the sum of the only ordered set of six cyclic 4-digit numbers for which 
each polygonal type: triangle, square, pentagonal, hexagonal, heptagonal, and 
octagonal, is represented by a different number in the set. 

'''

from utilities.specialNumbers import generateFromLambda

def createNumbers(f, polygonal):
	return [(str(i), polygonal) for i in  list(generateFromLambda(f, 159)) if 999 < i and i < 10000]

def isAvailableType(numberPolygonal, usedNumbers):
	return not numberPolygonal[1] in usedTypes(usedNumbers)

def isSearchedContinuation(numberPolygonal, usedNumbers):
	return len(usedNumbers) == 0 or numberPolygonal[0][:2] == searchedPrefix(usedNumbers)

def isPossibleContinuation(numberPolygonal, usedNumbers):
	return len(usedNumbers) < 6 and isAvailableType(numberPolygonal, usedNumbers) and isSearchedContinuation(numberPolygonal, usedNumbers)

def isSolutionFound(numberPolygonal, usedNumbers):
	return len(usedNumbers) == 6 and usedNumbers[0][0][:2] == numberPolygonal[0][2:]

def searchedPrefix(usedNumbers):
	return usedNumbers[-1][0][2:]

def usedTypes(usedNumbers):
	return [np[1] for np in usedNumbers]

def solveRecursively(usedNumbers, candidates):
	for numberPolygonal in candidates:
		if not isPossibleContinuation(numberPolygonal, usedNumbers):
			continue 
		usedNumbers.append(numberPolygonal)
		if isSolutionFound(numberPolygonal, usedNumbers):
			return True
		if solveRecursively(usedNumbers, [n for n in candidates if n != numberPolygonal]):
			return True
		usedNumbers.remove(numberPolygonal)
	return False

if __name__ == '__main__':
	trias = createNumbers(lambda n: n * (n + 1) // 2, "3")
	tetras = createNumbers(lambda n: n * n, "4")
	pentas = createNumbers(lambda n: n * (3 * n - 1) // 2, "5")
	hexas = createNumbers(lambda n: n * (2 * n - 1), "6")
	heptas = createNumbers(lambda n: n * (5 * n - 3) // 2, "7")
	octas = createNumbers(lambda n: n * (3 * n - 2), "8")

	numbers = trias + tetras + pentas + hexas + heptas + octas
	
	accumulator = []
	if solveRecursively(accumulator, numbers):
		print("Solution found:", accumulator)
		print("searched sum:", sum(int(n[0]) for n in accumulator))
		print("finished")
	else: 
		print("no solution")
 

