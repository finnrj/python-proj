'''

There are exactly ten ways of selecting three from five, 12345: 

123, 124, 125, 134, 135, 145, 234, 235, 245, and 345 

In combinatorics, we use the notation, 5C3 = 10. 

In general, 

 

nCr =  

n!r!(n−r)! 

'''

def pascals(maximum=100):
	i = 1
	pascal = [1]
	while i <= maximum:
		yield pascal
		pascal = [1] + [pascal[n] + pascal[n + 1] for n in range(len(pascal) - 1)] + [1]
		i += 1

if __name__ == '__main__':
	print(len([n for p in pascals(101) for n in p if n > 1000000]))
