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

import enchant


with open("cipher.txt") as fil:
	line = fil.readlines()[0]
	encryptedChars = line.split(',')[:-1]
	
def fetchChars():
	return [encryptedChars[count:count + 3] for count in range(0, len(encryptedChars) // 3, 3)]
		
def decryptTriple(key, triple):
	result = [chr(int(triple[i]) ^ key[i]) for i in range(3)]
	return "".join(result)
				
def fetchDecryptedWords(key, tripleCount):
	return ("".join([decryptTriple(key, triple) for triple in fetchChars()])).split()

if __name__ == '__main__':
	d = enchant.Dict("en_US")
	
	for key in itertools.product(string.ascii_lowercase, repeat=3):
		ords = [ord(ch) for ch in key]
		words = fetchDecryptedWords(ords, 30)
		if len(words) > 5 and  d.check(words[0]):  #  all(d.check(word) for word in words[:5])):
			print(key)
			print(words)		
 	
 	
