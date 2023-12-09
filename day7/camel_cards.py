# Advent of code day 7

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Find the winning hands")
parser.add_argument('filepath', type=Path, help="Game file")

args = parser.parse_args()

class Hand:
    max_hand_score = 13 * (13**4 + 13**3 + 13**2 + 13**1 + 13**0)

    def __init__(self, hand_str: str):
        parts = hand_str.strip().split(" ")
        self.bet = int(parts[1])
        self.hand_str = parts[0]

    def score(self) -> int:
        score = 0
        
        # Calculate the score based on card positions
        cards: dict[str, int] = {}
        for i, card in enumerate(reversed(self.hand_str)):
            cards.update({card: cards.get(card, 0) + 1})
            score += Hand._char_to_score(card) * 13 ** i

        # Add the hand score
        score += Hand._cards_to_hand_score(cards)
        return score
    
    def score_with_joker(self) -> int:
        score = 0
        
        # Calculate the score based on card positions
        cards: dict[str, int] = {}
        for i, card in enumerate(reversed(self.hand_str)):
            cards.update({card: cards.get(card, 0) + 1})
            score += Hand._char_to_score_joker(card) * 13 ** i
        
        if "J" in cards and len(cards) > 1:
            max_instances = 0
            mimic_card = ""
            for card_key in cards:
                if card_key != "J" and cards[card_key] > max_instances:
                    max_instances = cards[card_key]
                    mimic_card = card_key

            cards.update({mimic_card: cards[mimic_card] + cards.pop("J")})

        # Add the hand score
        score += Hand._cards_to_hand_score(cards)
        return score

    def _cards_to_hand_score(cards: dict[str, int]) -> int:
        unique_cards = len(cards)

        if unique_cards == 1: return 6 * Hand.max_hand_score # Five of a kind
        if unique_cards == 2:
            if 4 in cards.values(): return 5 * Hand.max_hand_score # Four of a kind
            return 4 * Hand.max_hand_score # Full house
        if unique_cards == 3:
            if 3 in cards.values(): return 3 * Hand.max_hand_score # Three of a kind
            return 2 * Hand.max_hand_score # Two pair
        if unique_cards == 4: return Hand.max_hand_score # One pair

        return 0

    def _char_to_score(char: str) -> int:
        if char.isdigit(): return int(char) - 1
        if char == "T": return 9
        if char == "J": return 10
        if char == "Q": return 11
        if char == "K": return 12
        if char == "A": return 13
    
    def _char_to_score_joker(char: str) -> int:
        if char.isdigit(): return int(char)
        if char == "T": return 10
        if char == "J": return 1
        if char == "Q": return 11
        if char == "K": return 12
        if char == "A": return 13

hands: list[Hand] = []
with open(args.filepath) as hands_file:
    
    
    for line in hands_file:
        hands.append(Hand(line))
    
    hands.sort(key=lambda hand: hand.score())

    winnings = 0
    for i, hand in enumerate(hands):
        winnings += (i + 1) * hand.bet
    
    print(f"Winnings (Part 1): {winnings}")

    hands.sort(key=lambda hand: hand.score_with_joker())

    winnings = 0
    for i, hand in enumerate(hands):
        winnings += (i + 1) * hand.bet
    
    print(f"Winnings with joker (Part 2): {winnings}")