'''

It can be seen that the number, 125874, and its double, 251748, contain exactly 
the same digits, but in a different order. 

Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x, 
contain the same digits. 

'''
from utilities.specialNumbers import isPermutation

def hasProperty(x):
	return all([isPermutation(i * x, encryptedChars=str(x)) for i in range(2, 7)])
	
if __name__ == '__main__':
	i = 99
	while True:
		i = i + 3
		if(int(str(i)[:2]) < 17 and hasProperty(i)):
			print ("found the bloody thing: %d" % i)
			break
		print(i)
