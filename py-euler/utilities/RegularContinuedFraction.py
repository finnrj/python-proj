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
from _pydecimal import _sqrt_nearest
from fractions import Fraction
from functools import reduce
from math import floor, sqrt


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
        lambda acc, a_i: Fraction(acc.denominator, a_i * acc.denominator + acc.numerator),
        reversed(regContFrac[1:-1]),
        Fraction(1, regContFrac[-1]))


def getRepeatingRegContFrac(sqrtArg):
    """ return list which represents a periodic continued fraction, where list[1:] is periodic
        m_0 = 0, d_0 = 1,  a_0 = _sqrt_nearest(sqrtArg), 
        m_(n+1) = d_n * a_n - m_n
        d_(n+1) = floor((sqrtArg - m_(n+1)^2) / d_n 
        a_(n+1) = (sqrtArg + m_(n+1)) / d_(n+1)
    """
    magic = []  # m_n, d_n, a_n
    a_0 = floor(sqrt(sqrtArg))
    nextTriple = (0, 1, a_0)
    
    
    while nextTriple not in magic:
        magic.append(nextTriple)
        
        old_m, old_d, old_a = magic[-1]
        m = old_d * old_a - old_m
        d = (sqrtArg - m ** 2) / old_d
        a = floor((a_0 + m) / d)
        nextTriple = (m, d, a)
    
    return [a for (m, d, a) in magic]

print(getRepeatingRegContFrac(2))    
print(getRepeatingRegContFrac(14))
