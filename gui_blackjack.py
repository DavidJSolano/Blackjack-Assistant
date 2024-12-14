import tkinter as tk
from tkinter import messagebox
from shuffling_deck import generate_deck, shuffle_all_decks
from blackjack import convert_to_tuples, calculate_hand_value

# Hi-Lo card counting values
hilo_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

def calculate_running_count(hand, running_count):
    for card in hand:
        rank = card[0]
        if rank in hilo_values:
            running_count += hilo_values[rank]
    return running_count

def true_count(running_count, remaining_decks):
    if remaining_decks == 0:
        return running_count
    return running_count / remaining_decks

def recommend_hilo_action(player_hand, dealer_hand, running_count, remaining_decks):
    true_count_value = true_count(running_count, remaining_decks)
    player_value = calculate_hand_value(player_hand)
    dealer_up_card = dealer_hand[0][0]

    if true_count_value >= 2:
        return "Stand" if player_value >= 12 else "Hit"
    elif true_count_value >= 1:
        return "Hit" if player_value <= 15 else "Stand"
    else:
        if player_value >= 13 or (player_value >= 12 and dealer_up_card in ['2', '3', '4', '5', '6']):
            return "Stand"
        else:
            return "Hit"

class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack with Hi-Lo Card Counting")
        self.initialize_game()
        self.create_widgets()
        self.start_game()

    def initialize_game(self):
        self.deck = []
        self.running_count = 0
        self.remaining_decks = 0
        self.player_hand = []
        self.dealer_hand = []

    def create_widgets(self):
        # Dealer Section
        tk.Label(self.root, text="Dealer's Hand:", font=("Helvetica", 14)).pack(pady=5)
        self.dealer_hand_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.dealer_hand_label.pack(pady=5)
        self.dealer_rank_label = tk.Label(self.root, text="Dealer's Hand Rank: ", font=("Helvetica", 12))
        self.dealer_rank_label.pack(pady=5)

        # Player Section
        tk.Label(self.root, text="Your Hand:", font=("Helvetica", 14)).pack(pady=5)
        self.player_hand_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.player_hand_label.pack(pady=5)
        self.player_rank_label = tk.Label(self.root, text="Your Hand Rank: ", font=("Helvetica", 12))
        self.player_rank_label.pack(pady=5)

        # Recommendation Section
        self.recommendation_label = tk.Label(self.root, text="Recommendation: ", font=("Helvetica", 14, "bold"), fg="blue")
        self.recommendation_label.pack(pady=10)

        # Buttons Section
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        self.hit_button = tk.Button(button_frame, text="Hit", command=self.hit)
        self.hit_button.pack(side=tk.LEFT, padx=10)
        self.stand_button = tk.Button(button_frame, text="Stand", command=self.stand)
        self.stand_button.pack(side=tk.LEFT, padx=10)

    def start_game(self):
        self.deck = shuffle_all_decks(generate_deck())
        self.deck = convert_to_tuples(self.deck)
        self.remaining_decks = len(self.deck) // 52
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.running_count = calculate_running_count(self.player_hand + self.dealer_hand, 0)
        self.update_display()

    def update_display(self):
        self.dealer_hand_label.config(text=f"{self.dealer_hand[0][0]} of {self.dealer_hand[0][1]} [Hidden]")
        self.player_hand_label.config(text=", ".join([f"{card[0]} of {card[1]}" for card in self.player_hand]))

        self.dealer_rank_label.config(text=f"Dealer's Hand Rank: {calculate_hand_value(self.dealer_hand)}")
        self.player_rank_label.config(text=f"Your Hand Rank: {calculate_hand_value(self.player_hand)}")

        self.recommendation_label.config(text=f"Recommendation: {recommend_hilo_action(self.player_hand, self.dealer_hand, self.running_count, self.remaining_decks)}")

    def hit(self):
        new_card = self.deck.pop()
        self.player_hand.append(new_card)
        self.running_count = calculate_running_count([new_card], self.running_count)
        self.update_display()

        if calculate_hand_value(self.player_hand) > 21:
            messagebox.showinfo("Game Over", "You busted! Dealer wins.")
            self.end_game()

    def stand(self):
        self.dealer_hand_label.config(text=", ".join([f"{card[0]} of {card[1]}" for card in self.dealer_hand]))
        while calculate_hand_value(self.dealer_hand) < 17 and len(self.deck) > 0:
            new_card = self.deck.pop()
            self.dealer_hand.append(new_card)
            self.running_count = calculate_running_count([new_card], self.running_count)
        self.update_display()
        self.check_winner()

    def check_winner(self):
        player_value = calculate_hand_value(self.player_hand)
        dealer_value = calculate_hand_value(self.dealer_hand)
        if dealer_value > 21 or player_value > dealer_value:
            messagebox.showinfo("Game Over", "You win!")
        elif player_value < dealer_value:
            messagebox.showinfo("Game Over", "Dealer wins!")
        else:
            messagebox.showinfo("Game Over", "It's a tie!")
        self.end_game()

    def end_game(self):
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        tk.Button(self.root, text="Restart", command=self.restart_game).pack(pady=10)

    def restart_game(self):
        self.root.destroy()
        root = tk.Tk()
        BlackjackGUI(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    BlackjackGUI(root)
    root.mainloop()
