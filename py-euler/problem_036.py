'''
The decimal number, 585 = 10010010012 (binary), is palindromic in both bases.

Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.

(Please note that the palindromic number, in either base, may not include leading zeros.)

'''



def isPalindrome(x):
    return str(x) == str(x)[::-1]

if __name__ == '__main__':
    print(sum([n for n in range(1, 1000000, 2) if isPalindrome(n) and isPalindrome(str(bin(n))[2:])]))
