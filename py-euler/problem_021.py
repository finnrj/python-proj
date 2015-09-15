'''
Created on Jun 2, 2015

'''
from math import factorial

# def someOfDiviors(x):
#     s = 1
#     for i in range(2, int(math.sqrt(x)) + 1):
#         if (x % i == 0):
#             s += i
#             s += x / i
#     return s

def divisors(x):
    return [j for j in range(1, x // 2 + 1) if x % j == 0]

if __name__ == '__main__':
    amicablesNumbers = []
    for i in range(1, 10000):
        a = sum(divisors(i))
        b = sum(divisors(a))
        if i < a and i == b:
            amicablesNumbers.extend([i, a])
            
    print(amicablesNumbers)
    print(sum(amicablesNumbers))
            
        
    
