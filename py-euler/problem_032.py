'''
We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once; for example, the 5-digit number, 15234, 
is 1 through 5 pandigital.

The product 7254 is unusual, as the identity, 39 × 186 = 7254, 
containing multiplicand, multiplier, and product is 1 through 9 pandigital.

Find the sum of all products whose multiplicand/multiplier/product identity can be written 
as a 1 through 9 pandigital.
HINT: Some products can be obtained in more than one way so be sure to only include 
it once in your sum.
'''

def isPandigital(a, b, c):
    s = str(a) + str(b) + str(c)
    if len(s) != 9:
        return False
    for c in "123456789":
        if c not in s:
            return False
    return True

if __name__ == '__main__':
  oneXfour = [(a, b, a * b) for a in range(1, 10) for b in range(1000, 10000) if isPandigital(a, b, a * b)]
  twoXthree = [(a, b, a * b) for a in range(10, 100) for b in range(100, 1000) if isPandigital(a, b, a * b)]
  print(oneXfour)
  print (len([t[2] for t in oneXfour + twoXthree]), len(set([t[2] for t in oneXfour + twoXthree])),
         sum(set([t[2] for t in oneXfour + twoXthree])))
  print([t[2] for t in oneXfour + twoXthree]) 
