'''

The nth term of the sequence of triangle numbers is given by, tn = ½n(n+1); so 
the first ten triangle numbers are: 

1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ... 

By converting each letter in a word to a number corresponding to its 
alphabetical position and adding these values we form a word value. For 
example, the word value for SKY is 19 + 11 + 25 = 55 = t10. If the word value 
is a triangle number then we shall call the word a triangle word. 

Using words.txt (right click and 'Save Link/Target As...'), a 16K text file 
containing nearly two-thousand common English words, how many are triangle 
words? 

'''

def getCHarValue(word):
    return sum([charVals[ch] for ch in word])

from string import ascii_uppercase

if __name__ == '__main__':
	with open("p042_words.txt") as fil:
		words = [name[1:-1] for line in fil.readlines() for name in line.split(",")]
		charVals = dict(zip(ascii_uppercase, range(1, len(ascii_uppercase) + 1)))

		triangleNumbers = set(0.5 * n * (n + 1) for n in range(1, 1000))
		print(len([w for w in words if getCHarValue(w) in triangleNumbers]))
