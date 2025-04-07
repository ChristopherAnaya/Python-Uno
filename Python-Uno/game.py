import random
import time

class Game:
    def __init__ (self):
        self.ready = False
        
        self.base_deck = [
        'yellow_0', 'yellow_1', 'yellow_1', 'yellow_2', 'yellow_2', 'yellow_3', 'yellow_3', 'yellow_4', 'yellow_4', 'yellow_5', 'yellow_5', 'yellow_6', 'yellow_6', 'yellow_7', 'yellow_7', 'yellow_8', 'yellow_8', 'yellow_9', 'yellow_9', 
        'yellow_block', 'yellow_block', 'yellow_reverse', 'yellow_reverse', 'yellow_plus2', 'yellow_plus2', 
        'green_0', 'green_1', 'green_1', 'green_2', 'green_2', 'green_3', 'green_3', 'green_4', 'green_4', 'green_5', 'green_5', 'green_6', 'green_6', 'green_7', 'green_7', 'green_8', 'green_8', 'green_9', 'green_9', 
        'green_block', 'green_block', 'green_reverse', 'green_reverse', 'green_plus2', 'green_plus2', 
        'red_0', 'red_1', 'red_1', 'red_2', 'red_2', 'red_3', 'red_3', 'red_4', 'red_4', 'red_5', 'red_5', 'red_6', 'red_6', 'red_7', 'red_7', 'red_8', 'red_8', 'red_9', 'red_9', 
        'red_block', 'red_block', 'red_reverse', 'red_reverse', 'red_plus2', 'red_plus2', 
        'blue_0', 'blue_1', 'blue_1', 'blue_2', 'blue_2', 'blue_3', 'blue_3', 'blue_4', 'blue_4', 'blue_5', 'blue_5', 'blue_6', 'blue_6', 'blue_7', 'blue_7', 'blue_8', 'blue_8', 'blue_9', 'blue_9', 
        'blue_block', 'blue_block', 'blue_reverse', 'blue_reverse', 'blue_plus2', 'blue_plus2', 'wild_change', 'wild_change', 'wild_change', 'wild_change', 'wild_plus4', 'wild_plus4', 'wild_plus4', 'wild_plus4']
        self.current_deck = self.base_deck.copy()
        card = random.randrange(0, len(self.current_deck) - 8)
        del self.current_deck[card]
        self.current_card = self.current_deck[card]

        self.played_cards = []
        self.played_cards.append([self.current_deck[card], 0, 0, 0])

        self.valid_cards = list(filter(lambda x: x.split("_")[0] == self.current_card.split("_")[0] or x.split("_")[1] == self.current_card.split("_")[1], self.base_deck)) + ['wild_change', 'wild_plus4']
       
        self.current_player = 1
        self.clockwise = True
    
        self.player_hands = {}
        for x in range(4):
            self.player_hands[f"player{x+1}"] = []
        for x in range(7):
            for y in range(4):
                card = random.randrange(0, len(self.current_deck))
                self.player_hands[f"player{y+1}"].append(self.current_deck[card])
                del self.current_deck[card]

        self.first = True
        self.time_left = 30.00
        self.pause = False

        for x in range(4):
            self.player_hands[f"player{x+1}"] = sorted(self.player_hands[f"player{x+1}"])

        self.update_player = self.current_player
 
    def sort(self):
        def card_key(card):
            parts = card.split("_", 1)  
            color = parts[0]
            rest = parts[1] if len(parts) > 1 else ""

            number_value = int(rest) if rest.isdigit() else float("inf")

            return (color, number_value)
        
        for x in range(4):
            self.player_hands[f"player{x+1}"] = sorted(self.player_hands[f"player{x+1}"], key=card_key)

    def time(self):
        self.start_time = time.time()

    def play(self, card):
        self.current_card = card
        self.played_cards.append([card, random.randint(-90, 90), random.randint(-10, 10), random.randint(-10, 10)])
        if "wild" in self.current_card:
            self.pause = True

            self.update_player = (self.update_player + (1 if self.clockwise else - 1)) % 5
            if self.update_player == 0:
                self.update_player = (1 if self.clockwise else 4)
            if len(self.played_cards) > 10:
                del self.played_cards[0]

            del self.player_hands[f"player{self.current_player}"][self.player_hands[f"player{self.current_player}"].index(card)]
        else:
            self.current_player = self.update_player
            if len(self.played_cards) > 10:
                del self.played_cards[0]
            del self.player_hands[f"player{self.current_player}"][self.player_hands[f"player{self.current_player}"].index(card)]
            self.valid_cards = list(filter(lambda x: x.split("_")[0] == self.current_card.split("_")[0] or x.split("_")[1] == self.current_card.split("_")[1], self.base_deck)) + ['wild_change', 'wild_plus4']
            
            if self.current_card.split("_")[1] == "reverse":
                self.clockwise = not self.clockwise
        
            if self.current_card.split("_")[1] == "plus2":
                self.current_player = (self.current_player + (1 if self.clockwise else - 1)) % 5
                if self.current_player == 0:
                    self.current_player = (1 if self.clockwise else 4)
                for x in range(2):
                    card = random.randrange(0, len(self.current_deck))
                    self.player_hands[f"player{self.current_player}"].append(self.current_deck[card])
                    del self.current_deck[card]

            if self.current_card.split("_")[1] == "block":
                self.current_player = (self.current_player + (1 if self.clockwise else - 1)) % 5

            if self.current_player == 0:
                self.current_player = (1 if self.clockwise else 4)

            self.current_player = (self.current_player + (1 if self.clockwise else - 1)) % 5

            if self.current_player == 0:
                self.current_player = (1 if self.clockwise else 4)
            
            self.update_player = self.current_player
            #self.sort()
            self.time()
    
    def draw(self):
        if not self.pause:
            card = random.randrange(0, len(self.current_deck))
            self.player_hands[f"player{self.current_player}"].append(self.current_deck[card])
            del self.current_deck[card]
            self.current_player = (self.current_player + (1 if self.clockwise else - 1)) % 5

            if self.current_player == 0:
                self.current_player = (1 if self.clockwise else 4)
            
            self.update_player = self.current_player
            #self.sort()
            self.time()

    def update_time(self):
        if not self.pause:
            if self.first:
                self.first = False
                self.time()
            self.time_left = round(time.time()- self.start_time, 2)
            if self.time_left >= 30:

                card = random.randrange(0, len(self.current_deck))
                self.player_hands[f"player{self.current_player}"].append(self.current_deck[card])
                del self.current_deck[card]
                self.current_player = (self.current_player + (1 if self.clockwise else - 1)) % 5

                if self.current_player == 0:
                    self.current_player = (1 if self.clockwise else 4)

                #self.sort() play outer wilds
                self.time()

    def wild_update(self, color):
        self.valid_cards = list(filter(lambda x: x.split("_")[0] == color, self.base_deck)) + ['wild_change', 'wild_plus4']
        self.current_player = self.update_player
        print(self.current_card)
        
        if self.current_card.split("_")[1] == "plus4":
            for x in range(4):
                card = random.randrange(0, len(self.current_deck))
                self.player_hands[f"player{self.current_player}"].append(self.current_deck[card])
                del self.current_deck[card]
            self.current_player = (self.current_player + (1 if self.clockwise else - 1)) % 5
            if self.current_player == 0:
                self.current_player = (1 if self.clockwise else 4)

        self.pause = False

        self.time()
        