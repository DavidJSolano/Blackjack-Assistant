from shuffling_deck import Card, generate_deck, shuffle_all_decks

values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

# Hi-Lo card counting values
hilo_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

def convert_to_tuples(deck):
    return [(card.rank, card.suit) for card in deck]

def calculate_hand_value(hand):
    value = 0
    ace_count = 0
    for card in hand:
        value += values[card[0]]
        if card[0] == 'A':
            ace_count += 1
    while value > 21 and ace_count:
        value -= 10
        ace_count -= 1
    return value

def display_hand(hand, hide_first_card=False):
    if hide_first_card:
        print("[hidden]", f"{hand[1][0]} of {hand[1][1]}")
    else:
        for card in hand:
            print(f"{card[0]} of {card[1]}", end=" | ")
        print()

def calculate_running_count(hand, running_count):
    """Calculate the running count based on the Hi-Lo system for the given hand."""
    for card in hand:
        rank = card[0]
        if rank in hilo_values:
            running_count += hilo_values[rank]
    return running_count

def true_count(running_count, remaining_decks):
    """Calculate the true count as the running count divided by the number of remaining decks."""
    if remaining_decks == 0:
        return running_count
    return running_count / remaining_decks

def recommend_hilo_action(player_hand, dealer_hand, running_count, remaining_decks):
    """Provide action recommendation (Hit or Stand) based on the Hi-Lo true count."""
    tc = true_count(running_count, remaining_decks)
    player_value = calculate_hand_value(player_hand)
    dealer_up_card = dealer_hand[0][0]

    # Simple example logic to demonstrate integration of Hi-Lo count into decisions
    if tc >= 2:
        return "Stand" if player_value >= 12 else "Hit"
    elif tc >= 1:
        return "Hit" if player_value <= 15 else "Stand"
    else:
        # Default basic logic when count is low
        if player_value >= 13 or (player_value >= 12 and dealer_up_card in ['2', '3', '4', '5', '6']):
            return "Stand"
        else:
            return "Hit"

def play_blackjack(num_decks=3):
    print("Welcome to Blackjack with Hi-Lo card counting!")
    print("Try to get as close to 21 as possible without going over!")
    print("You can 'hit' to take another card or 'stand' to keep your current hand.")
    print("We'll also provide Hi-Lo-based recommendations for hitting or standing.")
    print("-" * 60)

    all_decks = []
    for _ in range(num_decks):
        all_decks.extend(generate_deck())
    shuffled_deck = shuffle_all_decks(all_decks)
    deck = convert_to_tuples(shuffled_deck)

    # Track remaining decks for True Count calculation
    remaining_decks = len(deck) // 52

    player_hand = [deck.pop()]
    dealer_hand = [deck.pop()]
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())

    # Initial running count based on dealt cards
    running_count = calculate_running_count(player_hand + dealer_hand, 0)

    print("\nDealer's hand:")
    display_hand(dealer_hand, hide_first_card=True)

    print("\nYour hand (value:", calculate_hand_value(player_hand), "):")
    display_hand(player_hand)

    # Player's turn
    while calculate_hand_value(player_hand) < 21:
        # Provide a recommendation based on the current count
        recommendation = recommend_hilo_action(player_hand, dealer_hand, running_count, remaining_decks)
        print("Recommended action (Hi-Lo):", recommendation)
        
        move = input("Enter 'hit' or 'stand': ").lower()
        if move == 'hit':
            new_card = deck.pop()
            player_hand.append(new_card)
            running_count = calculate_running_count([new_card], running_count)
            remaining_decks = len(deck) // 52
            print("\nYou drew:", f"{player_hand[-1][0]} of {player_hand[-1][1]}")
            print("Your hand (value:", calculate_hand_value(player_hand), "):")
            display_hand(player_hand)
        elif move == 'stand':
            break
        else:
            print("Invalid input. Please enter 'hit' or 'stand'.")

    player_value = calculate_hand_value(player_hand)
    if player_value > 21:
        print("\nYou busted! Dealer wins.")
        return

    print("\nDealer's hand revealed:")
    display_hand(dealer_hand)
    while calculate_hand_value(dealer_hand) < 17:
        new_card = deck.pop()
        dealer_hand.append(new_card)
        running_count = calculate_running_count([new_card], running_count)
        remaining_decks = len(deck) // 52
        print("Dealer draws:", f"{dealer_hand[-1][0]} of {dealer_hand[-1][1]}")
        print("Dealer's hand (value:", calculate_hand_value(dealer_hand), "):")
        display_hand(dealer_hand)

    dealer_value = calculate_hand_value(dealer_hand)

    print("\nFinal Results:")
    print("Your value:", player_value)
    print("Dealer value:", dealer_value)
    if dealer_value > 21 or player_value > dealer_value:
        print("You win!")
    elif player_value < dealer_value:
        print("Dealer wins.")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    play_blackjack()
