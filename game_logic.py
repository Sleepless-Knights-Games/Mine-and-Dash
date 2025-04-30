import random
import uuid

class Game:
    def __init__(self, num_players=2):
        self.num_players = num_players
        self.round = 1
        self.turn = 1
        self.deck = []
        self.cave_in_deck = []
        self.hands = [[] for _ in range(num_players)]
        self.escape_cards = [self.make_card("Escape") for _ in range(num_players)]
        self.discard_pile = []
        self.cave_in_streak = 0
        self.cave_in_cards_revealed = []
        self.round_over = False
        self.all_treasures = (
            [self.make_card("Diamond") for _ in range(7)] +
            [self.make_card("Gold") for _ in range(8)] +
            [self.make_card("Emerald") for _ in range(12)] +
            [self.make_card("Sapphire") for _ in range(18)] +
            [self.make_card("Ruby") for _ in range(30)]
        )
        self.init_game()

    def make_card(self, name):
        return {"id": str(uuid.uuid4()), "name": name}

    def init_game(self):
        self.deck = self.all_treasures.copy()
        random.shuffle(self.deck)
        self.cave_in_deck = ["Cave-In"] * 5 + ["Safe"] * 15
        random.shuffle(self.cave_in_deck)
        for i in range(self.num_players):
            self.hands[i] = [self.deck.pop() for _ in range(4)] + [self.escape_cards[i]]
        self.turn = 1
        self.round_over = False
        self.cave_in_streak = 0
        self.cave_in_cards_revealed = []

    def play_card(self, card_id):
        self.turn += 1
        player_index = (self.turn - 2) % self.num_players
        hand = self.hands[player_index]
        card = next(c for c in hand if c["id"] == card_id)
        hand[:] = [c for c in hand if c["id"] != card_id]
        if card["name"] != "Escape":
            hand.append(self.deck.pop() if self.deck else self.make_card("Empty"))

        drawn = self.cave_in_deck.pop(0)
        if drawn == "Cave-In":
            self.cave
