'''
Created on Jun 2, 2015

@author: finn


'''


def collatz_chain(x):
    erg = [x]
    while x != 1:
        if x % 2 == 0:
            x //= 2
        else:
            x = 3 * x + 1
        erg.append(x)
        
    return erg
        
if __name__ == '__main__':
    maximum = (1, 1)
    for n in range(1, 1000000):
        candidate_length = len(collatz_chain(n))
        if (candidate_length > maximum[1]):
            maximum = (n, candidate_length)
            print(maximum)
    