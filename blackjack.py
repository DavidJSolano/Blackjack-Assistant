from shuffling_deck import Card, generate_deck, shuffle_all_decks

values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
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
        print("[hidden]", hand[1])
    else:
        for card in hand:
            print(f"{card[0]} of {card[1]}", end=" | ")
        print()

def play_blackjack(num_decks=3):
    print("Welcome to Blackjack!")
    print("Try to get as close to 21 as possible without going over!")
    print("You can 'hit' to take another card or 'stand' to keep your current hand.")
    print("-" * 50)

    all_decks = []
    for _ in range(num_decks):
        all_decks.extend(generate_deck())
    shuffled_deck = shuffle_all_decks(all_decks)
    deck = convert_to_tuples(shuffled_deck)

    player_hand = [deck.pop()]
    dealer_hand = [deck.pop()]
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())

    print("\nDealer's hand:")
    display_hand(dealer_hand, hide_first_card=True)

    print("\nYour hand (value:", calculate_hand_value(player_hand), "):")
    display_hand(player_hand)

    # Player's turn
    while calculate_hand_value(player_hand) < 21:
        move = input("Enter 'hit' or 'stand': ").lower()
        if move == 'hit':
            player_hand.append(deck.pop())
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
        dealer_hand.append(deck.pop())
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
