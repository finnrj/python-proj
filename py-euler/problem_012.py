'''
Created on Apr 21, 2015

@author: finn
'''

from utilities.divisors import countDivisors

def triangle(maximum=100000):
    n = 1
    s = n
    while n <= maximum:
        yield s
        n += 1 
        s += n
    
if __name__ == '__main__':
    for triangeNumber in triangle():
        if countDivisors(triangeNumber) > 500:
            print(triangeNumber)
            break
        
#     for i in triangle(10000):
#         print(i)
#         divisors = [j for j in range(1, i // 2 + 1) if i % j == 0]
#         divisors.append([i])
#         if len(divisors) > 500:
#             print(i, divisors)
#             break;

            
    
    
