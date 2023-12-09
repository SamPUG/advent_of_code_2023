# Advent of code day 1

import argparse
import math
from pathlib import Path

parser = argparse.ArgumentParser(description="Process Elve's Calibration Document")
parser.add_argument('filepath', type=Path, help="Path to calibration document.")
parser.add_argument('--count_strings', action="store_true", help="If true, string versions of numerics will be counted (part 2).")

args = parser.parse_args()

total_val = 0
numeric_strings = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}

numeric_max_lenth = 0
numeric_min_length: int = math.inf
for numeric_string in numeric_strings.keys():
    if len(numeric_string) > numeric_max_lenth: numeric_max_lenth = len(numeric_string)
    if len(numeric_string) < numeric_min_length: numeric_min_length = len(numeric_string)


def find_left_right(line: str) -> tuple[int, int]:
    left_val = ''
    right_val = ''

    left_ptr = 0
    right_ptr = numeric_min_length

    while left_ptr < len(line):
        if line[left_ptr].isdigit():
            if left_val:
                right_val = line[left_ptr]
            else: 
                left_val = line[left_ptr]

            left_ptr += 1
            right_ptr = left_ptr + numeric_min_length
            continue
        elif not args.count_strings:
            left_ptr += 1
            continue

        if right_ptr <= len(line):
            if right_ptr - left_ptr > numeric_max_lenth:
                left_ptr += 1
                right_ptr = left_ptr + numeric_min_length
                continue

            current_char = numeric_strings.get(line[left_ptr: right_ptr], "")

            if current_char:
                left_ptr += 1
                right_ptr = left_ptr + numeric_min_length

                if left_val:
                    right_val = current_char
                else: 
                    left_val = current_char
            else:
                right_ptr += 1
        else:
            left_ptr += 1
            right_ptr = left_ptr + numeric_min_length
    
    return (left_val, right_val)

with open(args.filepath) as calibration_file:
    for line in calibration_file:
        line = line.strip()
        left_val, right_val = find_left_right(line)

        total_val += int(left_val + (right_val if right_val else left_val))

print(f'Total calibration value is: {total_val}')




    

