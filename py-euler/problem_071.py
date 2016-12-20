'''

Consider the fraction, n/d, where n and d are positive integers. If nd and 
HCF(n,d)=1, it is called a reduced proper fraction. 

If we list the set of reduced proper fractions for d ≤ 8 in ascending order of 
size, we get: 

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 
3/4, 4/5, 5/6, 6/7, 7/8 

It can be seen that 2/5 is the fraction immediately to the left of 3/7. 

By listing the set of reduced proper fractions for d ≤ 1,000,000 in ascending 
order of size, find the numerator of the fraction immediately to the left of 
3/7. 

'''
from fractions import Fraction

if __name__ == '__main__':
	closestTo3_7 = 0
	three_seven = Fraction(3, 7)

	for d in range(1, 10 ** 6 + 1):
		n = int(3 * d / 7)
		n_d = Fraction(n, d)
		if n_d == three_seven:
			continue
		
		if three_seven - n_d < three_seven - closestTo3_7:
			closestTo3_7 = n_d
			print(closestTo3_7)
			
	print(closestTo3_7)
	print("finish")
