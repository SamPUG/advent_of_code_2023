# Advent of code day 9

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Make an oasis report reader")
parser.add_argument('filepath', type=Path, help="Oasis report")

args = parser.parse_args()

with open(args.filepath) as report_file:
    
    sum_futures = 0
    sum_pasts = 0
    for line in report_file:
        
        history = [int(val) for val in line.split()]
        last_vals = [history[-1]]
        first_vals = [history[0]]
        
        while any(history):
            history = [history[i] - history[i-1] for i in range(1, len(history))]
            last_vals.append(history[-1])
            first_vals.append(history[0])

        for i in range(-2, -len(last_vals) - 1 , -1): 
            last_vals[i] = last_vals[i] + last_vals[i+1] 
            first_vals[i] =  first_vals[i] - first_vals[i+1] 
        
        sum_futures += last_vals[0]
        sum_pasts += first_vals[0]

    print(f"Sum of futures (Part 1) is: {sum_futures}")
    print(f"Sum of pasts (Part 2) is: {sum_pasts}")