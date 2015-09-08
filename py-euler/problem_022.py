'''
Created on Jun 2, 2015

'''
import string

def valueOfName(name):
    return sum([ord(ch) - ord("A") + 1 for ch in name])

if __name__ == '__main__':
    with open("names.txt", mode='r') as fil:
        names = fil.readline().split(",")
        names = sorted([s.replace('"', '') for s in names])
        
    s = 0    
    for idx, name in enumerate(names):
        s += (idx + 1) * valueOfName(name)
    
    print(s)
    print(string.ascii_uppercase)
