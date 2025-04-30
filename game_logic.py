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

    def draw_card(self):
        return self.deck.pop() if self.deck else self.make_card("Empty")

    def play_card(self, card_id):
        player_index = (self.turn - 1) % self.num_players
        hand = self.hands[player_index]

        # Remove played card from hand
        card = next((c for c in hand if c["id"] == card_id), None)
        if card:
            hand[:] = [c for c in hand if c["id"] != card_id]

            if card["name"] != "Escape":
                hand.append(self.draw_card())

        # Draw from cave-in deck
        if self.cave_in_deck:
            drawn = self.cave_in_deck.pop(0)

            if drawn == "Cave-In":
                self.cave_in_streak += 1
                self.cave_in_cards_revealed.append("Cave-In")
            else:
                self.cave_in_streak = 0
                self.cave_in_cards_revealed.append("Safe")

                # Discard Safe and reshuffle Cave-Ins
                cave_ins_to_shuffle = [c for c in self.cave_in_cards_revealed if c == "Cave-In"]
                self.cave_in_deck += cave_ins_to_shuffle
                random.shuffle(self.cave_in_deck)

                # Clear revealed list after reshuffle
                self.cave_in_cards_revealed = []

            if self.cave_in_streak >= 3:
                self.round_over = True

        self.turn += 1

    def get_current_hand(self):
        player_index = (self.turn - 1) % self.num_players
        return self.hands[player_index]

    def next_round(self):
        if self.round < 3:
            self.round += 1
            self.init_game()

    def is_game_over(self):
        return self.round > 3

    def get_final_scores(self):
        # Placeholder scoring logic
        return {f"Player {i+1}": random.randint(10, 30) for i in range(self.num_players)}
