'''

All square roots are periodic when written as continued fractions and can be 
written in the form: 

 

√N = a0 + 

1 

'''
from math import floor, sqrt
 
def testPeriod(x, bucket, delta=0.000001):
	return True in [(abs(decs - x)) < delta for decs in bucket]

def testPeriod2(x, bucket, delta=0.000001):
	for decs in bucket:
		if((abs(decs - x)) < delta): 
			return True
	return False 


def doIt(root):
	n = sqrt(root)
	bucket = []
	while True:
		i = floor(n)
		decs = n - i
		if  testPeriod2(decs, bucket):
			print("root : %03d,  period: %d" % (root, len(bucket)))
			return len(bucket)
		bucket.append(decs)
		n = 1 / decs
	return bucket

if __name__ == '__main__':
	periods = [doIt(root) for root in range (2, 10001) if floor(sqrt(root)) != sqrt(root)]
	print(sum([(p % 2) for p in periods]))
	print(max(periods))


