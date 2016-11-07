'''
A regular continued Fraction has the following form:

a_0 + 1 / (a_1 + 1 / (... + 1 / a_k-1 + 1/a_k)

which is equivalent to

a_0 + 1
    ----------
           1
    a_1 + ------------
                  1
           a_2 + -------------
                   .
                   .
                   .
                   -----------------
                                 1
                        a_k-1 + ---
                                a_k

or

[a_0; a_1, a_2, ..., a_k]
'''
from math import floor, sqrt
from fractions import Fraction
from functools import reduce


def getRegularContinuedFraction(fraction):
    ''' Every fraction can be written as regular continued Fraction. For example:
        73/29 = 2 +15/29 expand with 1/15 so that numerator becomes 1
              = 2 + 1/(29/15)
              = 2 + 1/(1 + 14/15) expand with with 1/14 so that numerator becomes 1
              = 2 + 1/(1 + 1/(15/14))
              = 2 + 1/(1 + 1/(1 + 1/14)) we are finished because numerator is already 1
        return [2, 1, 1, 14] meaning [2; 1, 1, 14]
    '''
    regContFrac = []
    
    a_0 = floor(fraction)
    regContFrac.append(a_0)
    
    rest = fraction - a_0
    while rest.numerator > 1:
        newFraction = Fraction(rest.denominator, rest.numerator)
        a_i = floor(newFraction)
        regContFrac.append(a_i)
        rest = newFraction - a_i
    
    regContFrac.append(rest.denominator)
    return regContFrac

def regularContinuedFractionToFraction(regContFrac):
    if len(regContFrac) == 1:
        return regContFrac[0]
    
    return regContFrac[0] + reduce(
        lambda acc, a_i: Fraction(acc.denominator, a_i*acc.denominator+acc.numerator),
        reversed(regContFrac[1:-1]),
        Fraction(1, regContFrac[-1]))
    
def getRepeatingRegContFrac(sqrtX):
    ''' Every √x can be written through a repeating continues fraction. For example:
        √3 = 1 + √3 - 1
           = 1 + (√3 - 1) * 1
           = 1 + (√3 - 1) * (√3 + 1) / (√3 + 1) 
           = 1 + (3 - 1) / (√3 + 1) 
           = 1 + 2 / (√3 + 1) expand with 1/2 so that numerator becomes 1
           = 1 + 1 / (1/2 * (√3 + 1))
        The previous line is equal to √3. Therefore we can replace √3 with the whole line
           = 1 + 1 / (1/2 * ([1 + 1 / (1/2 * (√3 + 1))] + 1))
           = 1 + 1 / (1/2 * ([2 + 1 / (1/2 * (√3 + 1))]))
           = 1 + 1 / (1 + 1 / (√3 + 1)) numerator is already 1
        Replace √3 again in this term with the previous mentioned line
        ...
        Repeat until the continued Fraction repeats itself
        
        return [1, 1, 2] meaning the next number would have been already in there
    '''
    
    return pass
