# Advent of code day 6

import argparse
import math
from pathlib import Path
import re

parser = argparse.ArgumentParser(description="Win the race")
parser.add_argument('filepath', type=Path, help="Race files")

args = parser.parse_args()

class Race:
    def __init__(self, race_time: int = 0, record: int = 0):
        self.race_time = race_time
        self.record = record

    def ways_to_beat(self):
        root_part = math.sqrt(self.race_time ** 2 - 4 * self.record)
        root_part = root_part - 1 if root_part.is_integer() else root_part

        max_time = math.floor((self.race_time + root_part)/2)
        min_time = math.ceil((self.race_time - root_part)/2) 

        return max_time - min_time + 1

with open(args.filepath) as races_file:

    races = [Race(int(race_time)) for race_time in re.findall(r'\d+', races_file.readline())]

    multiplied_wins = 1

    for i, record_str in enumerate(re.findall(r'\d+', races_file.readline())):
        races[i].record = int(record_str)
        multiplied_wins *= races[i].ways_to_beat()

    print(f"Multiplied wins value (Part 1): {multiplied_wins}")

    long_race_time_str = ""
    long_record_time_str = ""

    for race in races:
        long_race_time_str += str(race.race_time)
        long_record_time_str += str(race.record)   

    long_race = Race(int(long_race_time_str), int(long_record_time_str))

    print(f"Long race win possibilities (Part 2): {long_race.ways_to_beat()}")
