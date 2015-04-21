'''
Created on Apr 21, 2015

@author: finn
'''


if __name__ == '__main__':
    for a in range(332, 1, -1):
        for b in range(332 + a, 1, -1):
            c = 1000 - b - a
            if a + b + c != 1000:
                print(a + b + c)
            
            if(a ** 2 + b ** 2 == c ** 2):
                print(a, b, c)
                print(a * b * c)

          

            
    
    
