# https://bicyclecards.com/how-to-play/blackjack/
# https://runestone.academy/runestone/books/published/pythonds/Introduction/ProgrammingExercises.html

# Make CPU random bets more realistic
# Fix 11 or 1 logic for Aces
# Method to check if hand is natural 21 +++
# Method to check all hands for natural 21 and make payouts +++
# Figure out how to end a round and make a player inactive for the rest of the while loop after a payout (think this can be done by just breaking the while loop if a condition is met within check_naturals() method) - can remove the player's hand, then when iterating through for turns check if player.hand exists and if not skip that player
# Remove a CPU player from game if they run out of chips. If user runs out of chips end the game entirely
# Handle the deck running out of cards by creating a new deck and reshuffling
# Figure out how to run through each players turns after checking naturals, and handle CPU logic for hits/stays based on the strategies outlined in the bicyle blackjack guide

import random
from collections import deque
import time


class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

        if isinstance(self.rank, int):
            self.value = self.rank
        elif self.rank in ['Jack', 'Queen', 'King']:
            self.value = 10
        else:
            self.value = [11, 1]

    def __repr__(self):
        return f'{self.rank} of {self.suit}'

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:

    suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']
    ranks = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King']

    def __init__(self):
        self.card_pile = deque([])
        self.discard_pile = []
        for s in Deck.suits:
            for v in Deck.ranks:
                self.card_pile.append(Card(v, s))

    def shuffle(self):
        random.shuffle(self.card_pile)
        print('The dealer shuffles the deck.')
        time.sleep(1)

    def deal(self):
        card1 = self.card_pile.popleft()
        card2 = self.card_pile.popleft()
        return [card1, card2]


class Hand(Deck):

    def __init__(self, deck, player, is_active):
        self.cards = deck.deal()
        self.deck = deck
        self.player = player
        self.is_active = is_active

    def hit(self):
        new_card = self.deck.card_pile.popleft()
        self.cards.append(new_card)

    def get_value(self):
        hand_value = 0
        aces = []
        for card in self.cards:
            if card.rank != 'Ace':
                hand_value += card.value
            else:
                aces.append(card)

        # Ace can be 11 or 1 depending on value of hand
        for ace in aces:
            if hand_value + ace.value[0] > 21:
                hand_value += ace.value[1]
            else:
                hand_value += ace.value[0]

        return hand_value

    def is_natural(self):
        if self.get_value() == 21:
            return True
        else:
            return False


class Player:

    def __init__(self, name, is_cpu, chips=50, hand=None, bet=None):
        self.name = name
        self.is_cpu = is_cpu
        self.chips = chips
        self.hand = hand
        self.bet = bet

    def place_bet(self, amt):
        self.bet = amt
        self.chips -= amt

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Dealer(Player):

    def __init__(self, name, is_cpu):
        super().__init__(name, is_cpu)
        self.hand = None

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Game:

    def __init__(self, title, num_opponents, min_bet=2, max_bet=500,
                 bets=None, players=None, user=None, dealer=None):
        self.title = title
        self.num_opponents = num_opponents
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.bets = bets
        self.players = players
        self.user = user
        self.dealer = dealer

    def create_players(self, name):
        self.user = Player(name, False)
        self.players = [Player(f'CPU{str(i+1)}', True) for i in range(self.num_opponents)]
        self.players.append(self.user)

        return random.shuffle(self.players)

    def list_cpus(self):
        for player in self.players:
            if player.is_cpu:
                print(player)

    def place_cpu_bets(self):
        for player in self.players:
            if player.is_cpu:
                player.place_bet(random.randint(self.min_bet, player.chips))

    def create_dealer(self):
        self.dealer = Dealer('Dealer', True)

    def deal_hands(self, deck):
        for player in self.players:
            player.hand = Hand(deck, player, True)
        self.dealer.hand = Hand(deck, self.dealer, True)
        print('Each player is dealt two cards.')
        print('The dealer is dealt two cards with one face down.')
        time.sleep(1)

    def show_hands(self):
        print('Dealer hand:')
        print([self.dealer.hand.cards[0], '?'])
        print('Hands and bets:')
        for player in self.players:
            print(f'{player.name}: {player.hand.cards} - Bet: {player.bet}')

    def show_chips(self):
        print('Player chips:')
        for player in self.players:
            print(f'{player.name} - Chips: {player.chips}')

    def check_naturals(self):
        # Returns True if round should be ended, False if continue round
        dealer_natural = self.dealer.hand.is_natural()
        for player in self.players:
            if player.hand.is_natural() and dealer_natural:
                player.chips += player.bet
                print(f'The dealer and {player.name} have a natural blackjack. {player.name} is returned their bet of {player.bet}.')
                player.bet = 0
            elif player.hand.is_natural():
                payout = player.bet * (3 / 2)
                player.chips += payout
                print(f'{player.name} has a natural blackjack. They are paid out {payout} chips.')
                player.bet = 0
                player.hand.is_active = False

        if dealer_natural:
            print('The dealer has a natural blackjack. The round is over and bets are forfeited.')
            return True

    def end_round(self):
        for player in self.players:
            player.hand = None

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title


def main():
    print('Welcome to Pythonic Blackjack!')
    game_title = input('Give your game a title: ')
    num_opps = int(input('How many opponents would you like to face? '))

    game = Game(game_title, num_opps)
    game.create_dealer()
    user_name = input('Dealer: Welcome to the table. What is your name? ')

    game.create_players(user_name)
    print(f'Howdy, {user_name}. The {num_opps} other players have arrived.')
    game.list_cpus()

    while True:
        input('Press enter to start the game.')
        time.sleep(1)

        game.show_chips()

        user_bet = int(input(f'Place your bets (min - {game.min_bet}, max - {game.max_bet}): '))
        game.user.place_bet(user_bet)
        game.place_cpu_bets()

        deck = Deck()
        deck.shuffle()

        game.deal_hands(deck)
        game.show_hands()

        dealer_natural = game.check_naturals()
        if dealer_natural:
            game.end_round()
            continue

        play_again = input('Play another hand? (y/n)')
        if play_again == 'y':
            continue
        else:
            break


if __name__ == "__main__":
    main()
