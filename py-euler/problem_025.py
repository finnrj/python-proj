'''
Created on Jun 2, 2015

'''
from itertools import permutations

def fib(max):
    a, b = 0, 1
    while True:
        yield b 
        if(len(str(b)) >= max):
            break
        a, b = b, a + b
    

if __name__ == '__main__':
    print(len(list(fib(1000))))
