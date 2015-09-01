'''
Created on Jun 2, 2015

'''

from datetime import date, timedelta


if __name__ == '__main__':
    
    sundaysOnFirstOfMonth = 0
    
    d = date(1901, 1, 6)

    while (d.year < 2001):
        if d.day == 1:
            sundaysOnFirstOfMonth += 1
        d += timedelta(days=7)
        
    print(sundaysOnFirstOfMonth)
        
    
