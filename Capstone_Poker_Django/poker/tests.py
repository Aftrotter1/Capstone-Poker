from django.test import TestCase
from .pokerhands import flush_value, evaluate_hand
from .hand_values import *
from .poker import Card

def get_cards(card_list):
    cards = []
    for name in card_list.split(','):
        rank, suit = name
        cards.append(Card(rank, suit))

    return cards

class TestEvaluateHand(TestCase):   #TODO: Long straight, 3 pairs, 2 sets of 3, 6-card flush, A-high straight, A-low straight
    def test_two_unalike(self):
        hand_value, quality = evaluate_hand(get_cards('4h,Kd'))
        self.assertEqual(hand_value, HIGH_CARD)
        self.assertEqual(quality, [12, 3])
        
    def test_two_alike(self):
        hand_value, quality = evaluate_hand(get_cards('6h,6c'))
        self.assertEqual(hand_value, PAIR)
        self.assertEqual(quality, [5, 5])
        
    def test_seven_straightflush(self):
        hand_value, quality = evaluate_hand(get_cards('4h,9c,8h,6h,5h,9s,7h'))
        self.assertEqual(hand_value, STRAIGHT_FLUSH)
        self.assertEqual(quality, [7, 6, 5, 4, 3])
        
    def test_seven_fourofakind(self):
        hand_value, quality = evaluate_hand(get_cards('Jh,Jc,Jd,6s,5h,Js,7h'))
        self.assertEqual(hand_value, FOUR_KIND)
        self.assertEqual(quality, [10, 10, 10, 10, 6])
        
    def test_seven_fullhouse(self):
        hand_value, quality = evaluate_hand(get_cards('Jh,7c,Jd,6s,5h,7s,7h'))
        self.assertEqual(hand_value, FULL_HOUSE)
        self.assertEqual(quality, [6, 6, 6, 10, 10])
        
    def test_seven_straightflush(self):
        hand_value, quality = evaluate_hand(get_cards('4h,9c,9h,6h,5h,9s,7h'))
        self.assertEqual(hand_value, FLUSH)
        self.assertEqual(quality, [8, 6, 5, 4, 3])
        
    def test_seven_straight(self):
        hand_value, quality = evaluate_hand(get_cards('4h,Jc,8h,6s,5h,Js,7h'))
        self.assertEqual(hand_value, STRAIGHT)
        self.assertEqual(quality, [7, 6, 5, 4, 3])
        
    def test_seven_threeofakind(self):
        hand_value, quality = evaluate_hand(get_cards('Kh,Jc,Jd,6s,5h,Js,7h'))
        self.assertEqual(hand_value, THREE_KIND)
        self.assertEqual(quality, [10, 10, 10, 12, 6])
        
    def test_seven_twopair(self):
        hand_value, quality = evaluate_hand(get_cards('Ah,2c,2d,6s,5h,As,7h'))
        self.assertEqual(hand_value, TWO_PAIR)
        self.assertEqual(quality, [13, 13, 1, 1, 6])
        
    def test_seven_pair(self):
        hand_value, quality = evaluate_hand(get_cards('Qh,2c,2d,6s,5h,As,7h'))
        self.assertEqual(hand_value, PAIR)
        self.assertEqual(quality, [1, 1, 13, 11, 6])
        
    def test_seven_highcard(self):
        hand_value, quality = evaluate_hand(get_cards('Qh,2c,9d,6s,5h,As,7h'))
        self.assertEqual(hand_value, HIGH_CARD)
        self.assertEqual(quality, [13, 11, 8, 6, 5])


class TestFlushValue(TestCase):
    def test_seven_straightflush(self):
        flush_val, vals = flush_value(get_cards('4h,9c,8h,6h,5h,9s,7h'))
        self.assertEqual(flush_val, 5)
        self.assertEqual(vals, [7, 6, 5, 4, 3])

