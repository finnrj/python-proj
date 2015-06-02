'''
Created on Apr 21, 2015

@author: finn
'''

def triangle(maximum):
    n = 1
    s = n
    while n <= maximum:
        yield s
        n += 1 
        s += n
    
if __name__ == '__main__':
    for i in triangle(10000):
        print(i)
        divisors = [j for j in range(1, i // 2 + 1) if i % j == 0]
        if len(divisors) >= 500:
            print(i, divisors)
            break;

            
    
    
