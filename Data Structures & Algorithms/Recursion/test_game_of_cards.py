import unittest
from game_of_cards import *


# Run from terminal: python -m unittest test_card.py
# Or, run the unittest.main()
class TestCard(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:

        self.ace_diamond = Card('A', 'D')
        self.ten_spade = Card('T', 'S')
        self.eight_heart = Card('8', 'H')
        self.eight_club = Card('8', 'C')

        self.deck = Deck()
        self.suits = ['C', 'D', 'H', 'S']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

        self.card_list = [Card('5', 'S'), Card('5', 'H'), Card('J', 'D'), Card('J', 'C'), Card('2', 'D'),
                          Card('2', 'H'),
                          Card('A', 'C'), Card('A', 'S'), Card('5', 'D'), Card('J', 'H'),
                          Card('5', 'C'), Card('8', 'H'), Card('8', 'D'), Card('J', 'S'), Card('6', 'H'),
                          Card('6', 'D'), Card('2', 'C'), Card('A', 'D'), Card('Q', 'S'), Card('8', 'C'),
                          Card('7', 'C'),
                          Card('3', 'H'), Card('7', 'S'), Card('3', 'S'), Card('K', 'D'), Card('4', 'S'),
                          Card('4', 'D'), Card('Q', 'H'),
                          Card('K', 'S'), Card('3', 'C'), Card('2', 'S'), Card('6', 'C'), Card('4', 'H'),
                          Card('A', 'H'), Card('9', 'C'), Card('9', 'H'),
                          Card('6', 'S'), Card('Q', 'D'), Card('8', 'C'), Card('K', 'H'), Card('K', 'C'),
                          Card('3', 'D'), Card('Q', 'C'), Card('9', 'S'), Card('4', 'C')]
        self.pile1 = Pile(self.card_list)

        self.pile2 = Pile()  # Empty

        self.pile3 = Pile([Card('4', 'C'), Card('K', 'S'), Card('K', 'D'),
                           Card('J', 'S'), Card('A', 'S'), Card('2', 'D')])

        self.pile4 = Pile([Card('7', 'C'), Card('5', 'S'), Card('J', 'H'), Card('T', 'H'), Card('7', 'H'),
                           Card('9', 'D'), Card('2', 'D'), Card('4', 'S'), Card('5', 'H'),
                           Card('7', 'S'), Card('9', 'C'), Card('3', 'H'), Card('8', 'D'),
                           Card('8', 'S'), Card('K', 'D'), Card('K', 'S'), Card('Q', 'C'),
                           Card('2', 'H'), Card('2', 'S'), Card('5', 'D')])  # 20 cards

        self.game = Game()

    """
    Unit test code for the Card class.
    """

    def test_card_init(self):
        self.assertEqual(self.ace_diamond.get_rank(), 'A')
        self.assertEqual(self.ace_diamond.get_suit(), 'D')

        self.assertEqual(self.ten_spade.get_rank(), 'T')
        self.assertEqual(self.ten_spade.get_suit(), 'S')

    def test_card_repr(self):
        self.assertEqual("Card(rank='A', suit='D')", repr(self.ace_diamond))
        self.assertEqual("Card(rank='8', suit='H')", repr(self.eight_heart))

    def test_card_str(self):
        self.assertEqual('AD', str(self.ace_diamond))
        self.assertEqual('8H', str(self.eight_heart))

    def test_card_eq(self):
        self.assertEqual(self.ace_diamond, Card('A', 'D'))
        self.assertEqual(self.ten_spade, Card('T', 'S'))

    def test_card_ne(self):
        self.assertTrue(self.ace_diamond != self.ten_spade)
        self.assertTrue(self.eight_heart != self.eight_club)

        self.assertFalse(self.ten_spade != self.ten_spade)
        self.assertFalse(self.eight_heart != self.eight_heart)

    def test_card_lt(self):
        self.assertTrue(self.ten_spade < self.ace_diamond)
        self.assertTrue(self.eight_club < self.eight_heart)

        self.assertFalse(self.ten_spade < self.eight_heart)
        self.assertFalse(self.ten_spade < Card('T', 'S'))

    def test_card_le(self):
        self.assertTrue(self.ten_spade <= self.ace_diamond)
        self.assertTrue(self.eight_club <= self.eight_heart)

        self.assertFalse(Card('J', 'S') <= self.ten_spade)
        self.assertFalse(Card('8', 'S') <= self.eight_heart)

    def test_card_gt(self):
        self.assertTrue(Card('A', 'S') > Card('A', 'H'))
        self.assertTrue(Card('J', 'H') > Card('J', 'D'))
        self.assertTrue(Card('T', 'D') > Card('T', 'C'))

        self.assertFalse(Card('K', 'S') > Card('A', 'S'))
        self.assertFalse(Card('T', 'H') > Card('J', 'H'))
        self.assertFalse(Card('9', 'D') > Card('T', 'D'))

    def test_card_ge(self):
        self.assertTrue(Card('A', 'S') >= Card('A', 'H'))
        self.assertTrue(Card('J', 'H') >= Card('J', 'D'))
        self.assertTrue(Card('T', 'C') >= Card('T', 'C'))

        self.assertFalse(Card('K', 'S') >= Card('A', 'S'))
        self.assertFalse(Card('T', 'H') >= Card('J', 'H'))
        self.assertFalse(Card('9', 'D') >= Card('T', 'D'))

    """
    Unit test code for the Deck class.
    """

    def test_deck_init(self):
        self.assertEqual(len(self.deck._cards), 52)
        i = 0
        for suit in self.suits:
            for rank in self.ranks:
                self.assertTrue(Card(rank, suit) == self.deck._cards[i])
                i += 1

    def test_deck_repr(self):
        deck = Deck()
        self.assertEqual('Deck()', repr(deck))

    def test_deck_str(self):
        deck = Deck()
        expected = """2C, 3C, 4C, 5C, 6C, \n7C, 8C, 9C, TC, JC, \nQC, KC, AC, 2D, 3D, 
4D, 5D, 6D, 7D, 8D, \n9D, TD, JD, QD, KD, \nAD, 2H, 3H, 4H, 5H, \n6H, 7H, 8H, 9H, TH, 
JH, QH, KH, AH, 2S, \n3S, 4S, 5S, 6S, 7S, \n8S, 9S, TS, JS, QS, \nKS, AS"""
        self.assertEqual(expected, str(deck))

    def test_deck_shuffle(self):
        self.deck.shuffle()
        self.assertEqual(len(self.deck._cards), 52)
        sorted_deck = Deck()
        self.assertTrue(self.deck != sorted_deck)
        for suit in self.suits:
            for rank in self.ranks:
                self.assertTrue(Card(rank, suit) in self.deck._cards)

    def test_deck_draw(self):
        card = self.deck.draw()
        self.assertEqual(len(self.deck._cards), 52 - 1)
        self.assertTrue(card not in self.deck._cards)

    """
    Unit test code for the Pile class.
    """

    def test_pile_init(self):
        self.assertIsInstance(self.pile1, Pile)
        self.assertIsInstance(self.pile2, Pile)
        self.assertEqual(self.pile2.pile_size(), 0)
        self.assertEqual(self.pile1.pile_size(), len(self.card_list))

    def test_pile_size(self):
        self.assertEqual(self.pile2.pile_size(), 0)
        self.assertEqual(self.pile1.pile_size(), len(self.card_list))

        pile = Pile([Card('5', 'S'), Card('5', 'H'), Card('J', 'D'), Card('J', 'C'), Card('2', 'D'), Card('2', 'H'),
                     Card('A', 'C'), Card('A', 'S')])
        self.assertEqual(pile.pile_size(), 8)

    def test_pile_draw(self):
        card = self.pile1.draw_card()
        self.assertEqual(self.pile1._size, len(self.card_list))
        self.assertTrue(card not in self.pile1._cards)

    def test_pile_add(self):
        pile = Pile([Card('A', 'H'), Card('K', 'S')])

        # Test adding one card
        one_card = Card('3', 'C')
        pile.add_cards(one_card)
        self.assertEqual(pile._size, 3)
        self.assertTrue(one_card in pile._cards)

        # Test adding a list of cards
        list_of_cards = [Card('A', 'D'), Card('7', 'H'),
                         Card('5', 'S'), Card('3', 'S'),
                         Card('J', 'C'), Card('5', 'D')]
        pile.add_cards(list_of_cards)
        self.assertEqual(pile._size, 9)
        self.assertTrue(Card('A', 'D') in pile._cards)
        self.assertTrue(Card('5', 'S') in pile._cards)
        self.assertTrue(Card('5', 'D') in pile._cards)

    def test_pile_find_highest(self):
        # No cards
        self.assertEqual(self.pile2.find_highest(), None)

        # Tied for highest
        tied = Pile([Card('4', 'C'), Card('K', 'S'), Card('K', 'D'),
                     Card('7', 'H'), Card('T', 'S'), Card('2', 'D')])
        self.assertEqual(tied.find_highest(), Card(rank='K', suit='S'))

        # One distinct highest
        pile = Pile([Card('9', 'H'), Card('A', 'D'), Card('K', 'S')])
        self.assertEqual(pile.find_highest(), Card('A', 'D'))

        self.assertEqual(self.pile3.find_highest(), Card('A', 'S'))

    def test_pile_most_common_suit(self):
        # No cards
        self.assertEqual(self.pile2.most_common_suit(), None)
        self.assertIsNone(self.pile2.most_common_suit(), None)

        # If suits tied
        tied = Pile([Card('4', 'C'), Card('K', 'S'), Card('K', 'D'),
                     Card('7', 'H'), Card('T', 'S'), Card('2', 'D')])
        self.assertEqual(tied.most_common_suit(), None)

        # One distinct common
        self.assertEqual(self.pile1.most_common_suit(), 'C')

        self.assertEqual(self.pile3.most_common_suit(), 'S')

    def test_get_pile(self):
        list_of_cards = [Card('A', 'H'), Card('K', 'S'), Card('6', 'C')]
        pile = Pile([Card('A', 'H'), Card('K', 'S'), Card('6', 'C')])
        returned = pile.get_pile()
        self.assertEqual(returned, list_of_cards)

        pile = Pile()
        returned = pile.get_pile()
        self.assertTrue(len(returned) == 0)
        self.assertEqual(returned, [])

    def test_pile_str(self):
        # Empty pile
        self.assertEqual('', str(self.pile2))

        # Mod3=1, 1 card
        pile = Pile([Card('A', 'D')])
        self.assertEqual(f"{str(Card('A', 'D'))}\n", str(pile))

        # Mod3=2, 2 cards
        pile = Pile([Card('A', 'D'), Card('8', 'C')])
        self.assertEqual("""AD\n8C\n""", str(pile))

        # Mod3=0, 6 cards
        self.assertEqual(
            """    4C
    KS
  KD  JS
AS      2D
""", str(self.pile3))

        # Mod3=1, 7 cards
        pile = Pile([Card('A', 'D'), Card('3', 'H'), Card('5', 'D'), Card('4', 'C'), Card('4', 'S'), Card('2', 'D'),
                     Card('J', 'D')])
        self.assertEqual("""    AD
    3H
    5D
  4C  4S
2D      JD
""", str(pile))

        # Mod3=2, 8 cards
        pile = Pile([Card('A', 'D'), Card('3', 'H'), Card('5', 'D'), Card('4', 'C'), Card('4', 'S'), Card('2', 'D'),
                     Card('J', 'D'), Card('6', 'H')])

        self.assertEqual("""    AD
    3H
    5D
    4C
  4S  2D
JD      6H
""", str(pile))

    """
    Unit test code for the Game class. 
    """

    def test_game_init(self):
        self.assertEqual(self.game._rounds, 0)

        self.assertEqual(self.game._player_draw_pile.pile_size(), 26)
        self.assertEqual(self.game._computer_draw_pile.pile_size(), 26)
        self.assertEqual(self.game._player_win_pile.pile_size(), 0)
        self.assertEqual(self.game._computer_win_pile.pile_size(), 0)

        self.assertEqual(len(self.game._wins), 0)
        self.assertEqual(self.game._player_peace_offerings, 0)
        self.assertEqual(self.game._computer_peace_offerings, 0)

    def test_print_winner(self):
        # Win piles same size (empty)
        self.assertEqual(self.game.print_winner(), "t")

        # Win piles different sizes, winner has smallest pile
        self.game._computer_win_pile.add_cards(Card('8', 'D'))
        self.assertEqual(self.game.print_winner(), "p")

        self.game._player_win_pile.add_cards([Card('2', 'C'), Card('J', 'H'), Card('5', 'C')])
        self.assertEqual(self.game.print_winner(), "c")

    def test_game_flow(self):
        print("Testing game flow")
        self.game = Game()

        self.game._player_draw_pile = Pile(
            [Card('2', 'C'), Card('8', 'S'), Card('T', 'H'), Card('7', 'D'), Card('4', 'C'),
             Card('4', 'D'), Card('9', 'D'), Card('9', 'H'),
             Card('5', 'S'), Card('A', 'C'), Card('3', 'D'), Card('8', 'H'),
             Card('6', 'S'), Card('K', 'D'), Card('K', 'H'), Card('T', 'S'),
             Card('J', 'H'), Card('2', 'D'), Card('6', 'D')])

        self.game._computer_draw_pile = Pile(
            [Card('3', 'C'), Card('T', 'D'), Card('T', 'C'), Card('7', 'C'), Card('4', 'H'), Card('A', 'H'),
             Card('7', 'H'),
             Card('9', 'S'), Card('6', 'C'), Card('4', 'S'),
             Card('7', 'S'), Card('9', 'C'), Card('3', 'H'), Card('8', 'D'),
             Card('K', 'S'), Card('8', 'C'), Card('A', 'S'), Card('Q', 'C'),
             Card('2', 'H')])
        self.game.start_game(7)
        '''
Testing game flow
====== Game of Cards ======

Round 1:
You have a 6D. The computer has a 2H.
You win. You collect the cards from this round.

Round 2:
You have a 2D. The computer has a QC.
The computer wins. It collects the cards from this round.

Round 3:
You have a JH. The computer has a AS.
The computer wins. It collects the cards from this round.

Round 4:
You have a TS. The computer has a 8C.
You win. You collect the cards from this round.

Round 5:
You have a KH. The computer has a KS.
Tie! You turned up a 3D. The computer turned up a 7S.
The computer wins and gives you its win pile as a peace offering.

Round 6:
You have a AC. The computer has a 4S.
You win. You collect the cards from this round.

Round 7:
You have a 5S. The computer has a 6C.
The computer wins. It collects the cards from this round.

GAME OVER.
The computer wins! It has the smallest win pile.

===== SUMMARY =====
Winner: Computer

Winner Breakdown:
Round 1 - Player
Round 2 - Computer
Round 3 - Computer
Round 4 - Player
Round 5 - Computer
Round 6 - Player
Round 7 - Computer

Peace Offerings:
By Player - 0
By Computer - 1
Highest Card - AS
Most Common Suit - None

Your Win Pile:
      6D
      2H
      TS
      8C
    2D  QC
  JH      AS
AC          4S


   '''


if __name__ == '__main__':
    unittest.main()
