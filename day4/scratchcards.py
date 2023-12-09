# Advent of code day 4

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Find the winning scratch cards")
parser.add_argument('filepath', type=Path, help="Scratchcard file.")

args = parser.parse_args()

class Card:
    def __init__(self, card_str: str):
        self.copies = 1

        game_strs = card_str.split(":")[1]
        game_strs = game_strs.split("|")

        nums = set(game_strs[0].replace("  ", " ").strip().split(" "))

        matches = 0
        
        for winning_num in game_strs[1].replace("  ", " ").strip().split(" "):
            if winning_num in nums:
                matches += 1
        
        self.matches = matches

    def calc_winnings(self):
        if (self.matches < 1): return 0
        return 2 ** (self.matches - 1)
    
    def make_copies(self, no_times: int) -> int:
        self.copies += no_times

total_winnings = 0
total_cards = 0

cards: list[Card] = []

with open(args.filepath) as scratchcard_file:
    for line in scratchcard_file:
        card = Card(line)
        cards.append(card)
        total_winnings += card.calc_winnings()

for i in range(len(cards)):
    for j in range(i + 1, i + cards[i].matches + 1):
        if j > len(cards): break
        cards[j].make_copies(cards[i].copies)
    
    total_cards += cards[i].copies

print(f"The pile of scratchcards is worth (Part 1): {total_winnings} points.")
print(f"Total cards (Part 2): {total_cards}.")