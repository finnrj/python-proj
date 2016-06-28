'''

Each character on a computer is assigned a unique code and the preferred 
standard is ASCII (American Standard Code for Information Interchange). For 
example, uppercase A = 65, asterisk (*) = 42, and lowercase k = 107. 

A modern encryption method is to take a text file, convert the bytes to ASCII, 
then XOR each byte with a given value, taken from a secret key. The advantage 
with the XOR function is that using the same encryption key on the cipher text, 
restores the plain text; for example, 65 XOR 42 = 107, then 107 XOR 42 = 65. 

For unbreakable encryption, the key is the same length as the plain text 
message, and the key is made up of random bytes. The user would keep the 
encrypted message and the encryption key in different locations, and without 
both "halves", it is impossible to decrypt the message. 

Unfortunately, this method is impractical for most users, so the modified 
method is to use a password as a key. If the password is shorter than the 
message, which is likely, the key is repeated cyclically throughout the 
message. The balance for this method is using a sufficiently long password key 
for security, but short enough to be memorable. 

Your task has been made easy, as the encryption key consists of three lower 
case characters. Using cipher.txt (right click and 'Save Link/Target As...'), a 
file containing the encrypted ASCII codes, and the knowledge that the plain 
text must contain common English words, decrypt the message and find the sum of 
the ASCII values in the original text. 



'''

import itertools
import string
import unittest

import enchant

dict = enchant.Dict("en_US")

with open("cipher.txt") as fil:
	line = fil.readlines()[0][:-1]
	encryptedChars = line.split(',')
	
def fetchChars(tripleCount, cipher):
	maximumTriples = min(tripleCount, len(cipher) // 3 + 1) 
	return [cipher[count * 3:(count + 1) * 3] for count in range(0, maximumTriples)]
		
def decryptTriple(key, triple):
	result = [chr(int(triple[i]) ^ key[i]) for i in range(len(triple))]
	return "".join(result)
				
def fetchDecryptedWords(key, tripleCount, cipher=encryptedChars):
	return ("".join([decryptTriple(key, triple) for triple in fetchChars(tripleCount, cipher)])).split()

def checkWord(word):
	if dict.check(word):
		return True
	if len(word) < 2:
		return False
	
	if not word[-1].isalpha():
		word = word[:-1]
		if dict.check(word):
			return True
	if not word[0].isalpha():
		word = word[1:]
	if len(word) == 0:
		return False
	return dict.check(word)
		
if __name__ == '__main__':
	for key in itertools.product(string.ascii_lowercase, repeat=3):
		ords = [ord(ch) for ch in key]
		words = fetchDecryptedWords(ords, 900)
		m = len(words)
		if len(words) < m:
			m = len(words)
# 	They did a typo -.- God.14 - missing space!!!
# 	allow up to 5% false words
		if [checkWord(w) for w in words[0:m]].count(False) / m < 0.05:
			print(key)
			print(" ".join(words))
			print(sum([ord(c) for c in " ".join(words)]))

	print("finished")

class TestCase(unittest.TestCase):
	
	def encrypt(self, key, text):
		cycledKey = key * (len(text) // 3 + 1)
		return [(ord(t[0]) ^ ord(t[1])) for t in zip(cycledKey, text)]
	
	def testEncryptLength(self):
		pass
		
	def testSanityTest(self):
		plain = "hubba dubba und eine Gurke"
		key = "bbc"
		encrypted = self.encrypt(key, plain)
		self.assertEquals(len(plain), len(encrypted))
		self.assertEqual(plain, " ".join(fetchDecryptedWords([ord(ch) for ch in key], 900, encrypted)))
		
	def testCheckWord(self):
		self.assertTrue(checkWord("(John)"))