'''

The square root of 2 can be written as an infinite continued fraction. 

 

√2 = 1 + 

1 

2; 1,2,1, 1,4,1, 1,6,1 
'''

from _functools import reduce
from fractions import Fraction
from utilities.RegularContinuedFraction import regularContinuedFractionToFraction


def getMagicNumbers(count=10):
	result = [2]
	a, b = divmod(count - 1, 3)
	triples = [(1, 2 * i, 1) for i in range(1, a + 1)]
	result = result + list(reduce(lambda t1, t2 : t1 + t2, triples))
	if b == 1:
		result.append(1)
	elif b == 2:
		result = result + [1, 2 * (a + 1)]
	return result

def magic(magicNumbers):
	return magicNumbers[0] + \
		reduce(
		lambda accumulator, nextMagicNumber: Fraction(1, nextMagicNumber + accumulator),
									reversed(magicNumbers[1:]),
									0)
	
def oldMagic(magicNumbers):
	if len(magicNumbers) == 1:
		return Fraction(1, magicNumbers[0])
	return Fraction(1, magicNumbers[0] + magic(magicNumbers[1:]))

if __name__ == '__main__':
	print(sum([int(ch) for ch in str(regularContinuedFractionToFraction(getMagicNumbers(100)).numerator)]))
	
	print(magic(getMagicNumbers()))
	print(sum([int(ch) for ch in str(magic(getMagicNumbers(100)).numerator)]))
	
