"""


implementing a card game using the Card, Deck, Pile, and Game classes. Recursion implementation
"""



RANK_ORDER = {
    '2': 2, '3': 3, '4': 4, '5': 5,
    '6': 6, '7': 7, '8': 8, '9': 9,
    'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

SUIT_ORDER = {
    'C': 0,  # clubs
    'D': 1,  # diamonds
    'H': 2,  # hearts
    'S': 3   # spades
}


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

    def __repr__(self):
        return f"Card(rank='{self.rank}', suit='{self.suit}')"

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def __eq__(self, other):
        return (self.rank == other.rank) and (self.suit == other.suit)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if RANK_ORDER[self.rank] < RANK_ORDER[other.rank]:
            return True
        elif RANK_ORDER[self.rank] == RANK_ORDER[other.rank]:
            return SUIT_ORDER[self.suit] < SUIT_ORDER[other.suit]
        else:
            return False

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        if RANK_ORDER[self.rank] > RANK_ORDER[other.rank]:
            return True
        elif RANK_ORDER[self.rank] == RANK_ORDER[other.rank]:
            return SUIT_ORDER[self.suit] > SUIT_ORDER[other.suit]
        else:
            return False

    def __ge__(self, other):
        return self > other or self == other


class Deck:
    def __init__(self):
        """
        Create a standard deck of 52 cards (no jokers) in ascending order:
       
        """
        self._cards = []
        suits = ['C', 'D', 'H', 'S']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

        for suit in suits:
            for rank in ranks:
                self._cards.append(Card(rank, suit))

    def __len__(self):
        return len(self._cards)

    def __repr__(self):
        return "Deck()"

    def __str__(self):
        """
        Return a multi-line string matching exactly what the tests say.
        """
        result = []
        for i, card in enumerate(self._cards):
            result.append(str(card))
            if i < 51:  # not the last card
                result.append(", ")
            if i in [4, 9, 14, 19, 24, 29, 34, 39, 44, 49]:
                result.append("\n")
        return "".join(result)

    def shuffle(self):
        """
        Shuffle by splitting in half and swapping.
        """
        half = len(self._cards) // 2
        self._cards = self._cards[half:] + self._cards[:half]

    def draw(self):
        """
        Remove and return the 'top' card (index 0). If empty, return None.
        """
        if not self._cards:
            return None
        return self._cards.pop(0)


class Pile:
    def __init__(self, cards=None):
        """
        Create a pile using the list of cards.
        If cards is missing, create an empty pile.
        """
        if cards is None:
            self._cards = []
        else:
            self._cards = list(cards)  # make a copy
        self._size = len(self._cards)

    def draw_card(self):
        """
        Remove and return the top card from the pile.
        """
        if self._cards:
            card = self._cards.pop(0)
            self._size = len(self._cards)
            return card
        return None

    def add_cards(self, cards):
        """
        Add a single Card object or a list of Card objects to the pile.
        """
        if isinstance(cards, Card):
            self._cards.append(cards)
        elif isinstance(cards, list):
            self._cards.extend(cards)
        self._size = len(self._cards)

    def pile_size(self):
        """
        Return the number of cards in the pile.
        """
        return self._size

    def find_highest(self):
        """
        Find and return (without removing) the highest card in the pile.
        Return None if the pile is empty.
        """
        if not self._cards:
            return None
        highest = self._cards[0]
        for card in self._cards:
            if card > highest:
                highest = card
        return highest

    def most_common_suit(self):
        """
        Return a string representing the most common suit in the pile.
        If there is a tie (or the pile is empty), return None.
        """
        if not self._cards:
            return None
        suit_counts = {}
        for card in self._cards:
            suit = card.get_suit()
            suit_counts[suit] = suit_counts.get(suit, 0) + 1

        max_count = None
        max_suit = None
        tie = False
        for suit, count in suit_counts.items():
            if max_count is None or count > max_count:
                max_count = count
                max_suit = suit
                tie = False
            elif count == max_count:
                tie = True
        return None if tie else max_suit

    def get_pile(self):
        """
        Return a copy of the list of cards in the pile.
        """
        return list(self._cards)

    def __str__(self):
        """
        Return a string representation of the pile as an inverted 'Y' (peace sign).

        This implementation uses the “remainder of three”:
          - n = the total number of cards.
          - q = n // 3 and r = n % 3.
          - The top section (vertical stem) will have T = q + r cards.
          - The bottom section will consist of B = q rows (each displaying two cards).
          - The top section is indented by 2*B spaces.
          - Each bottom row i (starting at 0) is printed with a left indent of (2*B - 2*(i+1)) spaces and a gap of (2 + 4*i) spaces between the two cards.
        """
        n = self._size
        if n == 0:
            return ""
        if n < 3:
            # For fewer than three cards, simply list one per line.
            return "".join(str(card) + "\n" for card in self._cards)
        
        q = n // 3          # Full groups of three
        r = n % 3           # Remainder (0, 1, or 2)
        T = q + r           # Top section count
        B = q               # Number of bottom rows
        top_indent = 2 * B
        lines = []
        # Print the top (vertical) section.
        for i in range(T):
            lines.append(" " * top_indent + str(self._cards[i]))
        # Print the bottom section (two cards per row).
        for i in range(B):
            li = top_indent - 2 * (i + 1)
            if li < 0:
                li = 0
            gap = 2 + 4 * i
            left_card = str(self._cards[T + 2 * i])
            right_card = str(self._cards[T + 2 * i + 1])
            lines.append(" " * li + left_card + " " * gap + right_card)
        return "\n".join(lines) + "\n"



class Game:
    def __init__(self):
        """
        creates two 26-card draw piles,
        empty win piles for both player and computer, and initializing other attributes.
        """
        self._rounds = 0
        deck = Deck()
        deck.shuffle()
        # Split the deck into two draw piles of 26 cards each.
        self._player_draw_pile = Pile(deck._cards[:26])
        self._computer_draw_pile = Pile(deck._cards[26:])
        self._player_win_pile = Pile()
        self._computer_win_pile = Pile()
        self._wins = []  # Record of round winners ("Player", "Computer", or "Tie")
        self._player_peace_offerings = 0
        self._computer_peace_offerings = 0

    def start_game(self, rounds):
        """
          - In a normal round, the higher-ranked card wins and the winner collects both cards.
          - In a tie, each player draws three cards (face down) and a fourth for a face-off.
            The player with the highest face-off card gives their win pile to the other as a peace offering.
          - Cards drawn during tie-break (face down and face off) are not added to any win pile.
        """
        print("====== Game of Cards ======\n")
        round_num = 1
        while (round_num <= rounds and
               self._player_draw_pile.pile_size() > 0 and
               self._computer_draw_pile.pile_size() > 0):
            print(f"Round {round_num}:")
            player_card = self._player_draw_pile.draw_card()
            computer_card = self._computer_draw_pile.draw_card()
            print(f"You have a {player_card}. The computer has a {computer_card}.")

            # Compare cards by rank only (using RANK_ORDER).
            player_rank = RANK_ORDER[player_card.get_rank()]
            computer_rank = RANK_ORDER[computer_card.get_rank()]
            if player_rank != computer_rank:
                if player_rank > computer_rank:
                    print("You win. You collect the cards from this round.\n")
                    self._player_win_pile.add_cards([player_card, computer_card])
                    self._wins.append("Player")
                else:
                    print("The computer wins. It collects the cards from this round.\n")
                    self._computer_win_pile.add_cards([player_card, computer_card])
                    self._wins.append("Computer")
            else:
                # Tie: each player must have at least 4 cards for tie-break.
                print("Tie!", end=" ")
                if (self._player_draw_pile.pile_size() < 4 or
                    self._computer_draw_pile.pile_size() < 4):
                    print("Not enough cards for tie-break. Ending game.\n")
                    break
                # Discard three cards from each pile.
                for _ in range(3):
                    self._player_draw_pile.draw_card()
                    self._computer_draw_pile.draw_card()
                # Draw the fourth card for face off.
                player_face = self._player_draw_pile.draw_card()
                computer_face = self._computer_draw_pile.draw_card()
                print(f"You turned up a {player_face}. The computer turned up a {computer_face}.")
                player_face_rank = RANK_ORDER[player_face.get_rank()]
                computer_face_rank = RANK_ORDER[computer_face.get_rank()]
                if player_face_rank > computer_face_rank:
                    print("You win and give your win pile to the computer as a peace offering.\n")
                    transferred = self._player_win_pile.get_pile()
                    self._computer_win_pile.add_cards(transferred)
                    self._player_win_pile = Pile()
                    self._wins.append("Player")
                    self._player_peace_offerings += 1
                elif player_face_rank < computer_face_rank:
                    print("The computer wins and gives you its win pile as a peace offering.\n")
                    transferred = self._computer_win_pile.get_pile()
                    self._player_win_pile.add_cards(transferred)
                    self._computer_win_pile = Pile()
                    self._wins.append("Computer")
                    self._computer_peace_offerings += 1
                else:
                    print("Face-off tie. No win pile exchange.\n")
                    self._wins.append("Tie")
            round_num += 1
            self._rounds += 1

        print("GAME OVER.")
        result = self.print_winner()
        self.summary(result)

    def print_winner(self):
        """
        Determines the overall winner (the one with the smallest win pile),
        returns:
          'p' for player win,
          'c' for computer win,
          't' for tie.
        """
        player_size = self._player_win_pile.pile_size()
        computer_size = self._computer_win_pile.pile_size()
        if player_size == computer_size:
            print("Tie! Both win piles are the same size.")
            return "t"
        elif player_size < computer_size:
            print("You win! You have the smallest win pile.")
            return "p"
        else:
            print("The computer wins! It has the smallest win pile.")
            return "c"

    def summary(self, result):
        """
        Prints a summary at the end of the game:
          - Overall winner and round-by-round winner breakdown.
          - The number of peace offerings made by each side.
          - The highest card and most common suit in the player's win pile.
          - The player's win pile displayed as an inverted 'Y' (peace sign).
        """
        print("\n===== SUMMARY =====")
        if result == "p":
            winner = "Player"
        elif result == "c":
            winner = "Computer"
        else:
            winner = "Tie"
        print(f"Winner: {winner}\n")
        print("Winner Breakdown:")
        for i, win in enumerate(self._wins, start=1):
            print(f"Round {i} - {win}")
        print("\nPeace Offerings:")
        print(f"By Player - {self._player_peace_offerings}")
        print(f"By Computer - {self._computer_peace_offerings}")
        highest = self._player_win_pile.find_highest()
        highest_str = str(highest) if highest is not None else "None"
        print(f"Highest Card - {highest_str}")
        most_common = self._player_win_pile.most_common_suit()
        most_common_str = most_common if most_common is not None else "None"
        print(f"Most Common Suit - {most_common_str}\n")
        print("Your Win Pile:")
        print(self._player_win_pile)



            


