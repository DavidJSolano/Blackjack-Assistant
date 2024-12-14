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
    """
    Update and return the running count for the given hand of cards.

    The running_count is adjusted based on the Hi-Lo system:
    - Low cards (2-6) add to the count.
    - High cards (10-Ace) subtract from the count.
    - 7, 8, 9 are neutral.
    """
    for card in hand:
        rank = card[0]
        if rank in hilo_values:
            running_count += hilo_values[rank]
    return running_count

def true_count(running_count, remaining_decks):
    """
    Calculate and return the true count by dividing the running count by 
    the number of remaining decks.

    True count provides a more accurate measure of card distribution 
    than running count alone.
    """
    if remaining_decks == 0:
        return running_count
    return running_count / remaining_decks

def recommend_hilo_action(player_hand, dealer_hand, running_count, remaining_decks):
    """
    Recommend an action ("Hit" or "Stand") based on the player's hand value, 
    the dealer's up card, and the Hi-Lo true count.

    The logic:
    - If the true count is high (>= 2), we tend to stand on lower player values 
      because the deck is 'rich' in high cards.
    - If the true count is slightly positive (>= 1), we might adjust our hitting/standing 
      threshold a bit more aggressively.
    - Otherwise, we fall back to a basic strategy that considers the player's 
      hand and the dealer's up card.
    """
    true_count_value = true_count(running_count, remaining_decks)
    player_value = calculate_hand_value(player_hand)
    dealer_up_card = dealer_hand[0][0]

    if true_count_value >= 2:
        # With a higher true count, if you have >=12, stand; otherwise, hit.
        return "Stand" if player_value >= 12 else "Hit"
    elif true_count_value >= 1:
        # Slightly positive count: hit if <=15, else stand.
        return "Hit" if player_value <= 15 else "Stand"
    else:
        # Neutral/negative count: follow a basic strategy based on dealer up card.
        if player_value >= 13 or (player_value >= 12 and dealer_up_card in ['2', '3', '4', '5', '6']):
            return "Stand"
        else:
            return "Hit"

class BlackjackGUI(QWidget):
    """
    A PyQt5-based graphical user interface for a Blackjack game utilizing 
    the Hi-Lo card counting system to provide hit/stand recommendations.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blackjack with Hi-Lo Card Counting")
        self.initialize_game()
        self.create_widgets()
        self.start_game()

    def initialize_game(self):
        """
        Initialize or reset game state variables.
        """
        self.deck = []
        self.running_count = 0
        self.remaining_decks = 0
        self.player_hand = []
        self.dealer_hand = []

    def create_widgets(self):
        """
        Create and set up all the UI elements in the main window.
        """
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
        """
        Set up a new game:
        - Shuffle the deck
        - Deal initial cards to player and dealer
        - Update the running and true counts
        - Refresh the display
        """
        self.deck = shuffle_all_decks(generate_deck())
        self.deck = convert_to_tuples(self.deck)
        self.remaining_decks = len(self.deck) // 52
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.running_count = calculate_running_count(self.player_hand + self.dealer_hand, 0)
        self.update_display()

    def update_display(self):
        """
        Update all labels to reflect the current state of the game:
        - Show dealer's partial hand (first card + hidden)
        - Show player's full hand
        - Show both hand values and recommended action
        """
        self.dealer_hand_label.setText(f"{self.dealer_hand[0][0]} of {self.dealer_hand[0][1]} [Hidden]")
        self.player_hand_label.setText(", ".join([f"{card[0]} of {card[1]}" for card in self.player_hand]))

        self.dealer_rank_label.setText(f"Dealer's Hand Rank: {calculate_hand_value(self.dealer_hand)}")
        self.player_rank_label.setText(f"Your Hand Rank: {calculate_hand_value(self.player_hand)}")

        recommendation = recommend_hilo_action(self.player_hand, self.dealer_hand, self.running_count, self.remaining_decks)
        self.recommendation_label.setText(f"Recommendation: {recommendation}")

    def hit(self):
        """
        Player chooses to hit:
        - Draw a card from the deck
        - Update counts and display
        - Check if player busts
        """
        if len(self.deck) == 0:
            QMessageBox.information(self, "Deck Empty", "No more cards in the deck!")
            return

        new_card = self.deck.pop()
        self.player_hand.append(new_card)
        self.running_count = calculate_running_count([new_card], self.running_count)
        self.update_display()

        # Check for bust
        if calculate_hand_value(self.player_hand) > 21:
            QMessageBox.information(self, "Game Over", "You busted! Dealer wins.")
            self.end_game()

    def stand(self):
        """
        Player chooses to stand:
        - Reveal dealer's hidden card
        - Dealer draws until reaching at least 17 or runs out of cards
        - Check winner
        """
        self.dealer_hand_label.setText(", ".join([f"{card[0]} of {card[1]}" for card in self.dealer_hand]))
        while calculate_hand_value(self.dealer_hand) < 17 and len(self.deck) > 0:
            new_card = self.deck.pop()
            self.dealer_hand.append(new_card)
            self.running_count = calculate_running_count([new_card], self.running_count)

        self.update_display()
        self.check_winner()

    def check_winner(self):
        """
        Determine the outcome once the dealer finishes drawing:
        - Compare player_value and dealer_value
        - Display a message for the outcome (win, lose, tie)
        - End the game
        """
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
        """
        Disable the Hit and Stand buttons and provide a Restart button.
        """
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)
        restart_button = QPushButton("Restart")
        restart_button.clicked.connect(self.restart_game)
        self.button_frame.layout().addWidget(restart_button)

    def restart_game(self):
        """
        Restart the game by opening a new window and closing the current one.
        Creating and showing the new window first ensures the app stays open.
        """
        self.new_window = BlackjackGUI()
        self.new_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlackjackGUI()
    window.show()
    sys.exit(app.exec_())
