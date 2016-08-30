'''

The 5-digit number, 16807=7**5, is also a fifth power. Similarly, the 9-digit 
number, 134217728=8**9, is a ninth power. 

How many n-digit positive integers exist which are also an nth power? 

'''

def getMaxPow():
	n = 1
	while True:
		n += 1
		if len(str(9 ** n)) < n :
			return n

if __name__ == '__main__':
	print(sum([len([s for s in range(10) if len(str(s ** n)) == n]) for n in range(1, getMaxPow())]))
