# Advent of code day 8

import argparse
from itertools import cycle
from math import lcm
from pathlib import Path

parser = argparse.ArgumentParser(description="Find Directions")
parser.add_argument('filepath', type=Path, help="Direction instructions.")

args = parser.parse_args()

with open(args.filepath) as direction_file:
    directions = direction_file.readline().strip()
    direction_file.readline() # read blank line

    direction_dict: dict[str, tuple[str, str]] = {}

    for line in direction_file:
        parts = line.split("=")
        lr_parts = parts[1].strip().split(", ")
        
        direction_dict[parts[0].strip()] = (lr_parts[0][1:], lr_parts[1][:3])
      
    current_nodes = [node for node in direction_dict.keys() if node.endswith("A")]
    steps = [0] * len(current_nodes)

    for i in range(len(current_nodes)):
        direction_cycle = cycle(directions)
        while not current_nodes[i].endswith("Z"):
            steps[i] += 1
            current_nodes[i] = direction_dict[current_nodes[i]][0] if next(direction_cycle) == "L" else direction_dict[current_nodes[i]][1]

    print(f"Steps to reach destination (Part 1): {steps[current_nodes.index('ZZZ')] }")
    print(f"Steps for all nodes to reach destination (Part 2): {lcm(*steps)}")