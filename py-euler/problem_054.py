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
		'''	cards = ([2H, 3D, KH, TS, 4C] ''' 		
		values = [self.ranks[card[0]] for card in cards]
		self.values = sorted(values, key=lambda val: (values.count(val), val), reverse=True)
		self.colors = [card[1] for card in cards]	
	
	def __str__(self):
		return "%s" % (self.values)

def hasPair(hand):
	return len(set(hand.values)) == 4

def hasTwoPairs(hand):
	return len(set(hand.values)) <= 3

def hasThreeOfAKind(hand):
	return hand.values.count(hand.values[0]) >= 3 or hand.values.count(hand.values[1]) >= 3 or hand.values.count(hand.values[2]) >= 3 

def hasStraight(hand):
	return hand.values[0] - hand.values[-1] == 4 and len(set(hand.values)) == 5 	

def hasFlush(hand):
	return len(set(hand.colors)) == 1

def hasFullHouse(hand):
	someValue = hand.values.count(hand.values[0])
	return len(set(hand.values)) == 2 and someValue >= 2 and someValue <= 3

def hasFourOfAKind(hand):
	return hand.values.count(hand.values[0]) == 4 or hand.values.count(hand.values[1]) == 4

def hasStraightFlush(hand):
	return hasFlush(hand) and hasStraight(hand)

def hasRoyalFlush(hand):
	return hasFlush(hand) and hasStraight(hand) and hand.values[0] == 14

rankMethods = [
			hasRoyalFlush,
			hasStraightFlush,
			hasFourOfAKind,
			hasFullHouse,
			hasFlush,
			hasStraight,
			hasThreeOfAKind,
			hasTwoPairs,
			hasPair]

def valuesToInt(hand):
	return int("".join(["%02d" % val for val in hand.values]))	
	
def getWinner(hands):
	hand0, hand1 = hands
	
	for rankMethod in rankMethods:
		if rankMethod(hand0) and not rankMethod(hand1):
			return 0
		if rankMethod(hand1) and not rankMethod(hand0):
			return 1
	return 0 if valuesToInt(hand0) > valuesToInt(hand1) else 1

if __name__ == '__main__':
	with open("utilities/poker.txt") as fil:
		deals = [(Hand(line.strip().split()[:5]), Hand(line.strip().split()[5:])) for line in fil.readlines() if line.strip()]
# 		for d1, d2 in deals:
# 			print(d1, d2)
		print(len(deals))
		print([getWinner(deal) for deal in deals].count(0))

class TestCase(unittest.TestCase):
	royalFlush = Hand(['AC', 'KC', 'QC', 'TC', 'JC'])
	straightFlush = Hand(['AC', 'KC', 'QC', 'TC', 'JC'])
	flush = Hand(['AC', 'KC', '2C', 'TC', 'JC'])
	fourOfAKind = Hand(['8C', '8D', '8S', '8H', '4S'])
	fullHouse = Hand(['AC', 'AH', 'AS', '8C', 'JC'])
	threeOfAKind = Hand(['8C', '8D', 'KC', '8H', '4S'])
	twoPairs = Hand(['8C', 'TS', 'TC', '8H', 'JS'])
	pair = Hand(['8C', 'TS', 'KC', '8H', '4S'])
		
	def testHasPair(self):
		self.assertTrue(hasPair(self.pair))
		self.assertFalse(hasPair(Hand(['9C', 'TS', 'KC', '8H', '4S'])))	

	def testHasTwoPairs(self):
		self.assertTrue(hasTwoPairs(self.twoPairs))
		self.assertFalse(hasTwoPairs(Hand(['8C', '4D', 'KC', '7H', '4S'])))
		self.assertTrue(hasTwoPairs(Hand(['8C', 'TS', 'TC', '8H', '8S'])))
		self.assertTrue(hasTwoPairs(Hand(['8C', 'TS', '8D', '8H', '8S'])))

	def testHasThreeOfAKind(self):
		self.assertTrue(hasThreeOfAKind(self.threeOfAKind))
		self.assertFalse(hasThreeOfAKind(Hand(['8C', 'TS', 'TC', '8H', '4S'])))
		self.assertTrue (hasThreeOfAKind(Hand(['8C', 'TS', 'TC', '8H', '8S'])))
		self.assertTrue (hasThreeOfAKind(Hand(['8C', 'TS', '8D', '8H', '8S'])))

	def testHasFlush(self):
		self.assertTrue(hasFlush(self.flush))
		self.assertFalse(hasFlush(Hand(['AC', 'KD', 'QC', '9C', 'JC'])))			
		
	def testHasFullHouse(self):
		self.assertFalse(hasFullHouse(self.fullHouse))
		self.assertFalse(hasFullHouse(Hand(['AC', 'AH', 'AS', 'AD', 'JC'])))
		self.assertTrue(hasFullHouse(Hand(['AC', 'AH', 'AS', '8C', '8H'])))
		
	def testHasFourOfAKind(self):
		self.assertTrue (hasFourOfAKind(self.fourOfAKind))
		self.assertFalse(hasFourOfAKind(Hand(['8C', 'TS', 'TC', '8H', '4S'])))
		self.assertFalse(hasFourOfAKind(Hand(['8C', 'TS', 'TD', '8H', 'TS'])))

	def testHasStraightFlush(self):
		self.assertTrue(hasStraightFlush(self.straightFlush))
		self.assertTrue(hasStraightFlush(Hand(['TC', 'KC', 'QC', '9C', 'JC'])))	
		self.assertFalse(hasStraightFlush(Hand(['TC', 'KC', '8C', '9C', 'JC'])))
		self.assertFalse(hasStraightFlush(Hand(['TC', 'KC', 'QD', '9C', 'JC'])))
				
	def testHasRoyalFlush(self):
		self.assertTrue(hasRoyalFlush(self.royalFlush))
		self.assertFalse(hasRoyalFlush(Hand(['9C', 'KC', 'QC', 'TC', 'JC'])))
		self.assertFalse(hasRoyalFlush(Hand(['AC', 'KC', 'QC', '9C', 'JC'])))	
		
	def testGetWinner(self):
		self.assertEqual(1, getWinner((self.straightFlush, self.royalFlush)))
		self.assertEqual(0, getWinner((self.straightFlush, self.fourOfAKind)))
		self.assertEqual(0, getWinner((self.fourOfAKind, self.fullHouse)))
		self.assertEqual(0, getWinner((self.fullHouse, self.pair)))
		self.assertEqual(1, getWinner((Hand(['9C', 'KD', 'QC', 'TS', '2C']), self.pair)))
		self.assertEqual(1, getWinner((Hand(['9C', '4D', '6C', '7S', '2C']), Hand(['9D', '3D', '5C', '8S', '2C']))))
		self.assertEqual(0, getWinner((Hand(['9C', '9H', '9D', '2S', '2C']), Hand(['8D', '8C', '8H', 'AS', 'AC']))))
		print(Hand(['QC', 'TH', 'TD', '8S', '5C']), Hand(['JD', 'JC', '8H', '6S', '2C']))
		self.assertEqual(1, getWinner((Hand(['QC', 'TH', 'TD', '8S', '5C']), Hand(['JD', 'JC', '8H', '6S', '2C']))))
	
	if __name__ == '__main__':
		unittest.main()
	
		
		
