'''

In the card game poker, a hand consists of five cards and are ranked, from 
lowest to highest, in the following way: 

High Card: Highest value card. 

One Pair: Two cards of the same value. 

Two Pairs: Two different pairs. 

Three of a Kind: Three cards of the same value. 

Straight: All cards are consecutive values. 

Flush: All cards of the same suit. 

Full House: Three of a kind and a pair. 

Four of a Kind: Four cards of the same value. 

Straight Flush: All cards are consecutive values of same suit. 

Royal Flush: Ten, Jack, Queen, King, Ace, in same suit. 

The cards are valued in the order:2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, 
King, Ace. 

If two players have the same ranked hands then the rank made up of the highest 
value wins; for example, a pair of eights beats a pair of fives (see example 1 
below). But if two ranks tie, for example, both players have a pair of queens, 
then highest cards in each hand are compared (see example 4 below); if the 
highest cards tie then the next highest cards are compared, and so on. 

Consider the following five hands dealt to two players: 

 

Hand Player 1 Player 2 Winner 

1 5H 5C 6S 7S KDPair of Fives 

8C TS KC 9H 4S 7D 2S 5D 3S AC
5C AD 5D AC 9C 7C 5H 8D TD KS
3H 7H 6S KC JS QH TD JC 2D 8S
TH 8H 5C QS TC 9H 4D JC KS JS
7C 5H KC QH JD AS KH 4C AD 4S
5H KS 9C 7D 9H 8D 3S 5D 5C AH
6H 4H 5C 3H 2H 3S QH 5S 6S AS
TD 8C 4H 7C TC KC 4C 3H 7S KS
7C 9C 6D KD 3H 4C QS QC AC KH
JC 6S 5H 2H 2D KD 9D 7C AS JS

'''
import string
import unittest


class Hand:
	ranks = dict(zip(string.digits[2:] + "TJQKA", range(2, 15))) 
	
	def __init__(self, cards):
		self.values = sorted([self.ranks[card[0]] for card in cards], reverse=True)
		self.colors = [card[1] for card in cards]	
	
	def __str__(self):
		return "%s, %s" % (self.values, self.colors)

def hasPair(hand):
	return len(set(hand.values)) == 4

if __name__ == '__main__':
	with open("utilities/poker.txt") as fil:
		hands = [(Hand(line.strip().split()[:5]), Hand(line.strip().split()[5:]))  for line in fil.readlines()]
		print ([str(h) for h in hands[0]])


def hasStraight(hand):
	return hand.values[0] - hand.values[-1] == 4 and len(set(hand.values)) == 5 	

def hasRoyalFlush(hand):
	return len(set(hand.colors)) == 1 and hasStraight(hand)

def hasFullHouse(hand):
	someValue = hand.values.count(hand.values[0])
	return len(set(hand.values)) == 2 and someValue >= 2 and someValue <= 3

class TestCase(unittest.TestCase):

	def testHasPair(self):
		self.assertTrue(hasPair(Hand(['8C', 'TS', 'KC', '8H', '4S'])))
		self.assertFalse(hasPair(Hand(['9C', 'TS', 'KC', '8H', '4S'])))	

	def testHasRoyalFlush(self):
		self.assertTrue(hasRoyalFlush(Hand(['AC', 'KC', 'QC', 'TC', 'JC'])))
		self.assertFalse(hasRoyalFlush(Hand(['AC', 'KC', 'QC', '9C', 'JC'])))	

	def testHasFullHouse(self):
		self.assertFalse(hasFullHouse(Hand(['AC', 'AH', 'AS', '8C', 'JC'])))
		self.assertFalse(hasFullHouse(Hand(['AC', 'AH', 'AS', 'AD', 'JC'])))
		self.assertTrue(hasFullHouse(Hand(['AC', 'AH', 'AS', '8C', '8H'])))
		
	if __name__ == '__main__':
		unittest.main()
	
		
		
