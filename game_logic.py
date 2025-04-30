import random

class Game:
    def __init__(self, num_players=2):
        self.num_players = num_players
        self.round = 1
        self.turn = 1
        self.deck = []
        self.cave_in_deck = []
        self.hands = [[] for _ in range(num_players)]
        self.escape_cards = ["Escape"] * num_players
        self.discard_pile = []
        self.cave_in_streak = 0
        self.cave_in_cards_revealed = []
        self.round_over = False
        self.all_treasures = ["Diamond"] * 7 + ["Gold"] * 8 + ["Emerald"] * 12 + ["Sapphire"] * 18 + ["Ruby"] * 30 + ["Special"] * 8
        self.init_game()

    def init_game(self):
        self.deck = self.all_treasures.copy()
        random.shuffle(self.deck)
        self.cave_in_deck = ["Cave-In"] * 5 + ["Safe"] * 15
        random.shuffle(self.cave_in_deck)
        for i in range(self.num_players):
            self.hands[i] = [self.draw_card() for _ in range(4)] + [self.escape_cards[i]]
        self.turn = 1
        self.round_over = False
        self.cave_in_streak = 0
        self.cave_in_cards_revealed = []

    def draw_card(self):
        return self.deck.pop() if self.deck else "Empty"

    def play_card(self, card):
        self.turn += 1
        player_index = (self.turn - 1) % self.num_players
        self.hands[player_index].remove(card)
        if card != "Escape":
            self.hands[player_index].append(self.draw_card())
        # Cave-in check
        drawn = self.cave_in_deck.pop(0)
        if drawn == "Cave-In":
            self.cave_in_streak += 1
            self.cave_in_cards_revealed.append("Cave-In")
        else:
            self.cave_in_streak = 0
            self.cave_in_cards_revealed.append("Safe")
        if self.cave_in_streak >= 3:
            self.round_over = True

    def get_current_hand(self):
        player_index = (self.turn - 1) % self.num_players
        return self.hands[player_index]

    def next_round(self):
        if self.round >= 3:
            return
        self.round += 1
        self.init_game()

    def is_game_over(self):
        return self.round > 3

    def get_final_scores(self):
        # Dummy scoring for now
        return {f"Player {i+1}": random.randint(10, 30) for i in range(self.num_players)}
