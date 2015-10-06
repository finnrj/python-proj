'''
Created on Jun 2, 2015

'''
powers = dict([(a, a ** 5) for a in range(0, 10)])

def getExponent():
    n = 1
    while n * (9 ** 5) > 10 ** n:
        n += 1
    return n

def digitSums(n):
    return sum([powers[int(c)] for c in str(n)])

if __name__ == '__main__':
    maxNumber = getExponent()
    print(sum([n for n in range(2, 10 ** maxNumber) if digitSums(n) == n]))
