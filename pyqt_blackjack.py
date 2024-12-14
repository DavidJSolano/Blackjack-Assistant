import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QMessageBox, QFrame)
from PyQt5.QtCore import Qt

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

class BlackjackGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blackjack with Hi-Lo Card Counting")
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
        self.layout = QVBoxLayout()

        # Title
        title_label = QLabel("Blackjack with Hi-Lo Card Counting")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size:16pt; font-weight:bold;")
        self.layout.addWidget(title_label)

        # Instructions
        instruction_label = QLabel("Try to get as close to 21 as possible without going over.\n"
                                   "Hi-Lo recommendations are provided to guide your decisions.")
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setStyleSheet("font-size:10pt;")
        self.layout.addWidget(instruction_label)

        # Dealer Frame
        dealer_frame = QFrame()
        dealer_frame_layout = QVBoxLayout()
        dealer_label = QLabel("Dealer's Hand:")
        dealer_label.setStyleSheet("font-size:14pt; font-weight:bold;")
        dealer_frame_layout.addWidget(dealer_label)

        self.dealer_hand_label = QLabel("")
        self.dealer_hand_label.setStyleSheet("font-size:14pt;")
        dealer_frame_layout.addWidget(self.dealer_hand_label)

        self.dealer_rank_label = QLabel("Dealer's Hand Rank: ")
        self.dealer_rank_label.setStyleSheet("font-size:12pt;")
        dealer_frame_layout.addWidget(self.dealer_rank_label)

        dealer_frame.setLayout(dealer_frame_layout)
        self.layout.addWidget(dealer_frame)

        # Player Frame
        player_frame = QFrame()
        player_frame_layout = QVBoxLayout()
        player_label = QLabel("Your Hand:")
        player_label.setStyleSheet("font-size:14pt; font-weight:bold;")
        player_frame_layout.addWidget(player_label)

        self.player_hand_label = QLabel("")
        self.player_hand_label.setStyleSheet("font-size:14pt;")
        player_frame_layout.addWidget(self.player_hand_label)

        self.player_rank_label = QLabel("Your Hand Rank: ")
        self.player_rank_label.setStyleSheet("font-size:12pt;")
        player_frame_layout.addWidget(self.player_rank_label)

        player_frame.setLayout(player_frame_layout)
        self.layout.addWidget(player_frame)

        # Recommendation Label
        self.recommendation_label = QLabel("Recommendation: ")
        self.recommendation_label.setStyleSheet("font-size:14pt; font-weight:bold; color:blue;")
        self.layout.addWidget(self.recommendation_label)

        # Buttons Section
        self.button_frame = QFrame()
        button_layout = QHBoxLayout()
        self.hit_button = QPushButton("Hit")
        self.hit_button.clicked.connect(self.hit)
        button_layout.addWidget(self.hit_button)

        self.stand_button = QPushButton("Stand")
        self.stand_button.clicked.connect(self.stand)
        button_layout.addWidget(self.stand_button)

        self.button_frame.setLayout(button_layout)
        self.layout.addWidget(self.button_frame)

        self.setLayout(self.layout)

    def start_game(self):
        self.deck = shuffle_all_decks(generate_deck())
        self.deck = convert_to_tuples(self.deck)
        self.remaining_decks = len(self.deck) // 52
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.running_count = calculate_running_count(self.player_hand + self.dealer_hand, 0)
        self.update_display()

    def update_display(self):
        self.dealer_hand_label.setText(f"{self.dealer_hand[0][0]} of {self.dealer_hand[0][1]} [Hidden]")
        self.player_hand_label.setText(", ".join([f"{card[0]} of {card[1]}" for card in self.player_hand]))

        self.dealer_rank_label.setText(f"Dealer's Hand Rank: {calculate_hand_value(self.dealer_hand)}")
        self.player_rank_label.setText(f"Your Hand Rank: {calculate_hand_value(self.player_hand)}")

        self.recommendation_label.setText(f"Recommendation: {recommend_hilo_action(self.player_hand, self.dealer_hand, self.running_count, self.remaining_decks)}")

    def hit(self):
        if len(self.deck) == 0:
            QMessageBox.information(self, "Deck Empty", "No more cards in the deck!")
            return

        new_card = self.deck.pop()
        self.player_hand.append(new_card)
        self.running_count = calculate_running_count([new_card], self.running_count)
        self.update_display()

        if calculate_hand_value(self.player_hand) > 21:
            QMessageBox.information(self, "Game Over", "You busted! Dealer wins.")
            self.end_game()

    def stand(self):
        self.dealer_hand_label.setText(", ".join([f"{card[0]} of {card[1]}" for card in self.dealer_hand]))
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
            QMessageBox.information(self, "Game Over", "You win!")
        elif player_value < dealer_value:
            QMessageBox.information(self, "Game Over", "Dealer wins!")
        else:
            QMessageBox.information(self, "Game Over", "It's a tie!")
        self.end_game()

    def end_game(self):
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)
        restart_button = QPushButton("Restart")
        restart_button.clicked.connect(self.restart_game)
        self.button_frame.layout().addWidget(restart_button)

    def restart_game(self):
        # Close current window and open a new one
        self.new_window = BlackjackGUI()
        self.new_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlackjackGUI()
    window.show()
    sys.exit(app.exec_())
