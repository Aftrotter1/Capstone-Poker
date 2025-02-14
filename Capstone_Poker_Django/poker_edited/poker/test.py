from poker import Card, Hand, Table, Pot
from pokerhands import evaluate_hand, is_straight
from pokerstrat import Cole
BLINDS = [10, 20]

# print(evaluate_hand([Card('3', 'h'), Card('5', 'h'), Card('A', 'c'), Card('7', 'h'), Card('9', 'h'), Card('10', 'h'), Card('2', 'h')]))
# print(evaluate_hand([Card('3', 'h'), Card('5', 'h'), Card('J', 'c'), Card('7', 'h'), Card('9', 'h'), Card('10', 'h'), Card('2', 'h')]))
# print(evaluate_hand([Card('3', 'h'), Card('5', 'h'), Card('J', 'c'), Card('7', 'h'), Card('9', 'h'), Card('J', 'h'), Card('2', 'h')]))
# print(evaluate_hand([Card('8', 'h'), Card('10', 'h'), Card('J', 'c'), Card('7', 'h'), Card('9', 'h'), Card('J', 'h'), Card('2', 'h')]))
# print(evaluate_hand([Card('8', 'h'), Card('10', 'h'), Card('8', 'c'), Card('8', 'd'), Card('9', 'h'), Card('8', 'c'), Card('2', 'h')]))
# print(evaluate_hand([Card('8', 'h'), Card('10', 'h'), Card('8', 'c'), Card('8', 'd'), Card('9', 'h'), Card('10', 'c'), Card('2', 'h')]))
# print(evaluate_hand([Card('8', 'h'), Card('10', 'h'), Card('8', 'c'), Card('8', 'd'), Card('9', 'h'), Card('K', 'c'), Card('2', 'h')]))
# print(evaluate_hand([Card('8', 'd'), Card('10', 'h'), Card('J', 'c'), Card('7', 'h'), Card('9', 'h'), Card('J', 'd'), Card('2', 'h')]))
# print(evaluate_hand([Card('2', 'd'), Card('10', 'h'), Card('J', 'c'), Card('7', 'h'), Card('9', 'h'), Card('J', 'd'), Card('2', 'h')]))
# print(evaluate_hand([Card('2', 'd'), Card('10', 'h'), Card('J', 'c'), Card('7', 'h'), Card('9', 'h'), Card('A', 'd'), Card('2', 'h')]))

table = Table()
pot = Pot(table, 'p')
hand = Hand('cole', table, 'Cole')
hand.add(Card('3', 'h'))
hand.add(Card('J', 'c'))
table.add(Card('4', 'h'))
table.add(Card('5', 'h'))
table.add(Card('7', 'd'))
table.add(Card('8', 's'))
table.add(Card('6', 'd'))
cole = Cole(hand)
cole.decide_play(hand, pot)