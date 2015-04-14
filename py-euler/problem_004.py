'''
Created on Apr 14, 2015

@author: finn
'''

def is_palindrome(n):
    return str(n) == str(n)[::-1]

if __name__ == '__main__':
    erg = 0
    x = 999
    y = 999
    while y > 0:
        if is_palindrome(x * y):
            if(x * y > erg):
                erg = x * y
                print(erg)
            x = 999
            y -= 1
        else:
            x -= 1
            if x < 1:
                x = 999
                y -= 1
                
    print(erg)
    print(sorted([(x, y, x * y) for x in range(1000, 99, -1) for y in range(x, 99, -1) if is_palindrome(x * y)], key=lambda a : a[2], reverse=True))    
