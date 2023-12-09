# Advent of code day 3

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Find the part numbers")
parser.add_argument('filepath', type=Path, help="Engine file.")

args = parser.parse_args()

file_list: list[str] = []

def is_symbol(char: str) -> bool:
    if char.isalnum(): return False
    if char == ".": return False
    return True

with open(args.filepath) as calibration_file:
    for line in calibration_file:
        file_list.append(line.strip())

total = 0
gears: dict[int, list[int]]= {} 

for line_no, line in enumerate(file_list):
    
    start_ptr = 0
    end_ptr = 1

    while end_ptr < len(line) + 1:
        if line[start_ptr].isnumeric():
            if end_ptr == len(line) or not line[end_ptr].isnumeric():
                # There is a complete number covered by the two pointers
                val = int(line[start_ptr:end_ptr])

                is_part_no = False

                for val_i in range(start_ptr, end_ptr):
                    if is_part_no: break
                    for i in range(val_i - 1, val_i + 2):
                        if is_part_no: break
                        for j in range(line_no - 1, line_no + 2):
                            if i >= 0 and i < len(line) and j >= 0 and j < len(file_list):
                                if is_symbol(file_list[j][i]):
                                    is_part_no = True
                                    if file_list[j][i] == "*":
                                        gear_key = (len(line) * j) + i
                                        gears[gear_key] = gears.get(gear_key, []) + [val]
                                    break

                if is_part_no: total += val

                start_ptr = end_ptr
                end_ptr = start_ptr + 1
    
            else: 
                end_ptr += 1
        else:
            start_ptr += 1
            end_ptr += 1

gear_ratio_sum = 0

for gear_vals in gears.values():
    if len(gear_vals) > 1:
        ratio = 1
        for gear_val in gear_vals:
            ratio *= gear_val
        gear_ratio_sum += ratio

print(f"Total of part numbers is: {total}")
print(f"Sum of gear ratios: {gear_ratio_sum}")

