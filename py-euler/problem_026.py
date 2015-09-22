'''
Created on Jun 2, 2015

'''
from itertools import permutations

def lengthOfRecurringCycle(d):
    rests = [10 % d]
    
    while rests[-1] != 0:
        newRest = (rests[-1] * 10) % d

        if newRest in rests:
            return len(rests)
        
        rests.append(newRest)

    return 0
    

if __name__ == '__main__':
    print(max([(lengthOfRecurringCycle(i), i) for i in range(2, 1001)]))
