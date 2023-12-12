# Advent of code day 11

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Do some astronomy")
parser.add_argument('filepath', type=Path, help="Galaxy file.")

args = parser.parse_args()

class Galaxy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.orig_x = x
        self.orig_y = y

    def reset(self):
        self.x = self.orig_x
        self.y = self.orig_y

galaxies: list[Galaxy] = []
empty_row_indexes: list[int] = []

with open(args.filepath) as galaxy_file:
    y = 0
    for line in galaxy_file:
        line = line.strip()
        if not y > 0:
            cols_empty = [True] * len(line)

        row_empty = True
        for x, char in enumerate(line):
            if char == "#":
                galaxies.append(Galaxy(x, y))
                row_empty = False
                cols_empty[x] = False
        
        if row_empty: empty_row_indexes.append(y)

        y += 1
    
    empty_before_x: int = [0] * len(cols_empty)
    for i in range(1, len(empty_before_x)):
        if cols_empty[i - 1]:
            empty_before_x[i] = empty_before_x[i-1] + 1
        else:
            empty_before_x[i] = empty_before_x[i-1]

    empty_before_y: int = [0] * y
    read_index = 0
    for i in range(1, len(empty_before_y)):
        if read_index < len(empty_row_indexes) and i - 1 == empty_row_indexes[read_index]:
            empty_before_y[i] = empty_before_y[i-1] + 1
            read_index += 1
        else:
            empty_before_y[i] = empty_before_y[i-1]

    sum_shortest = 0
    for i in range(len(galaxies)):
        galaxies[i].x += empty_before_x[galaxies[i].x]
        galaxies[i].y += empty_before_y[galaxies[i].y]

    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            sum_shortest += abs(galaxies[i].x - galaxies[j].x) + abs(galaxies[i].y - galaxies[j].y)

    print(f"Sum shortest (Part 1): {sum_shortest}")

    for i in range(len(galaxies)):
        galaxies[i].reset()

    sum_shortest = 0
    multiplier = 1000000
    for i in range(len(galaxies)):
        galaxies[i].x += empty_before_x[galaxies[i].x] * (multiplier - 1)
        galaxies[i].y += empty_before_y[galaxies[i].y] * (multiplier - 1)
        
    for i in range(len(galaxies)):    
        for j in range(i + 1, len(galaxies)):
            sum_shortest += abs(galaxies[i].x - galaxies[j].x) + abs(galaxies[i].y - galaxies[j].y)

    print(f"Sum shortest (Part 2): {sum_shortest}")