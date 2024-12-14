from dataclasses import dataclass
from typing import List
import random

@dataclass
class Card: 
    suit: str
    rank: str

def generate_deck() -> List[Card]:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return [Card(suit, rank) for suit in suits for rank in ranks]

def shuffle(deck: List[Card], rng: random.Random) -> List[Card]:
    """Shuffle a deck by interleaving two halves randomly."""
    half1 = deck[:len(deck) // 2]
    half2 = deck[len(deck) // 2:]
    
    shuffled = []
    while half1 or half2:
        if half1 and (not half2 or rng.random() > 0.5):
            shuffled.append(half1.pop(0))
        if half2 and (not half1 or rng.random() > 0.5):
            shuffled.append(half2.pop(0))
    
    return shuffled

def shuffle_all_decks(all_decks: List[Card], num_shuffles: int = 5) -> List[Card]:
    """Perform multiple shuffles on the combined decks."""
    deck = all_decks.copy()
    rng = random.Random()
    rng.seed()

    for _ in range(num_shuffles):
        deck = shuffle(deck, rng)
    
    return deck

def main():
    # For demonstration, generate a deck and shuffle it multiple times
    deck = generate_deck()
    print("Original Deck:")
    for card in deck:
        print(card)
    
    shuffled_deck = shuffle_all_decks(deck)
    print("\nShuffled Deck:")
    for card in shuffled_deck:
        print(card)

if __name__ == "__main__":
    main()
