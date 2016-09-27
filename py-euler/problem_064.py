'''

All square roots are periodic when written as continued fractions and can be 
written in the form: 



'''
from math import floor, sqrt

class ContinuedFraction:
    """ (sqrt(n) - a) / b """
    
    def __init__(self, n, a, b):
        self.n = n;
        self.a = a;
        self.b = b;
        
    def __str__(self):
        return "(sqrt(%d) + %d) / %d" % (self.n, self.a, self.b) 
    
    def __eq__(self, otherContFrac):
        return self.a==otherContFrac.a and self.b==otherContFrac.b # self.n==othreContFrac is implied
        
def getFirstContinuedFraction(n):
    """ sqrt(n)
    	let i := floor(sqrt(n))
        -> i + sqrt(n) - i
        -> i + 1/1/(sqrt(n) - i) 
        
        - only consider 1/(sqrt(n) - i) and extend it with 1/(sqrt(n) + i)
        let b := (sqrt(n) - i) * (sqrt(n) + i)
        -> (sqrt(n) + i) / b
        let pulledOut := floor((sqrt(n) + i) / b)
        let a = i - pulledOut * b
    """
    
    i = floor(sqrt(n))
    b = n - i**2 # don't use (sqrt(n) - i) * (sqrt(n) + i) cause of bad rounding!!!
    pulledOut = floor((sqrt(n) + i) / b)
    a = i - pulledOut * b
    return ContinuedFraction(n, a, b)

def getNextContinuedFraction(contFrac):
    """ let c := contFrac(n, a, b) = (sqrt(n) + a) / b
        -> 1/1/c -> 1 / (b / (sqrt(n) + a) )
        
        - only consider b / (sqrt(n) + a) and extend it with (sqrt(n) - a)
        let b'= (sqrt(n) + a) * (sqrt(n) - a)
        -> (b * (sqrt(n) - a)) / b' 
        -> reduce this fraction to (sqrt(n) - a) / b''
        let pulledOut := floor((sqrt(n) - a) / b'')
        let a' = -a - pulledOut * b''
        result is pulledOut + (sqrt(n) -a') / b''
        
    """
    bPrime = contFrac.n - contFrac.a**2
    bPrimePrime = bPrime / contFrac.b 
    pulledOut = floor((sqrt(contFrac.n) - contFrac.a) / bPrimePrime)
    aPrime = (-1)*contFrac.a - pulledOut * bPrimePrime
    return ContinuedFraction(contFrac.n, aPrime, bPrimePrime)
    
def getAllFractions(n):
    bucket = [getFirstContinuedFraction(n)]
    while True:
        nextContFrac = getNextContinuedFraction(bucket[-1])
        if(nextContFrac in bucket):
            return bucket
        else:
            bucket.append(nextContFrac)
            
    return bucket

def isIrrationalSquare(x):
    return not(floor(sqrt(x)) - sqrt(x) == 0)

if __name__ == '__main__':
    lenOfPeriods = [len(getAllFractions(i)) for i in range(2, 10001) if isIrrationalSquare(i)]
    print("max period is: %d" % max(lenOfPeriods))
    print("solution is: %d" % sum([l % 2 for l in lenOfPeriods]))


