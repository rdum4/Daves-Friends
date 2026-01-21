import unittest

from deck import *

class TestValidCards(unittest.TestCase):
	def test_wilds(self):
		deck = Deck()
		deck.add_default_cards()
		
		for card in deck.cards:
			self.assertTrue(can_play_card(card, Wild()))
			self.assertTrue(can_play_card(card, DrawFourWild()))
	def test_identical_cards(self):
		deck = Deck()
		deck.add_default_cards()
		
		for card in deck.cards:
			self.assertTrue(can_play_card(card, card))
	def test_special(self):
		deck = Deck()
		deck.add_default_cards()
		
		kinds = [Skip(Color.BLUE), Reverse(Color.BLUE), DrawTwo(Color.BLUE)]
		
		for kind in kinds:
			for card in deck.cards:
				if card.color == Color.BLUE:
					self.assertTrue(can_play_card(card, kind))
				elif type(card) == type(kind):
					self.assertTrue(can_play_card(card, kind))
				else:
					self.assertFalse(can_play_card(card, kind))
    
if __name__ == '__main__':
    unittest.main()
