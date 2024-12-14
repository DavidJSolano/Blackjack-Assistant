from dataclasses import dataclass
from typing import List

@dataclass
class Card: 
    suit: str
    rank: str

def generate_deck() -> List[Card]:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return [Card(suit, rank) for suit in suits for rank in ranks]

def main():
    deck = generate_deck()
    for card in deck:
        print(card)

if __name__ == "__main__":
    main()
