'''
Created on Apr 14, 2015

@author: finn
'''

def fibo(upto):
    a, b = 1, 1
    while b < upto:
        yield b
        a, b = b, a + b


if __name__ == '__main__':
    print(sum([n for n in fibo(4000000) if n % 2 == 0]))
