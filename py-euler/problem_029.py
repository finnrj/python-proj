'''
Created on Jun 2, 2015

'''
if __name__ == '__main__':
    print(len(set([a ** b for a in range(2, 101) for b in range(2, 101)])))
