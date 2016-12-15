'''
Created on Oct 7, 2015

@author: expert
'''

def isPermutation(n, encryptedChars="123456789"):
    s = str(n)
    if len(s) != len(encryptedChars):
        return False
#     return all(c in encryptedChars and encryptedChars.count(c) == s.count(c) for c in s)
    result = True
    for c in s:
        if not c in encryptedChars or encryptedChars.count(c) != s.count(c):
            return False
    return result

def generateFromLambda(f, count=10000):
    n = 1
    while n <= count:
        yield f(n)
        n += 1
        
def isPalindrome(x):
    return str(x) == str(x)[::-1]

        
if __name__ == '__main__':
    print(list(generateFromLambda(lambda n: n * (n + 1) // 2, 20)))
            
