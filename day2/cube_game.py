# Advent of code day 2

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Check for valid games")
parser.add_argument('filepath', type=Path, help="Game file.")

args = parser.parse_args()

MAX_RED_CUBES = 12
MAX_GREEN_CUBES = 13
MAX_BLUE_CUBES = 14

class Draw: 
    def __init__(self, draw_str: str):
        self.red_cubes = 0
        self.green_cubes = 0
        self.blue_cubes = 0

        cube_strs = draw_str.split(", ")

        for cube_str in cube_strs:
            cube_str = cube_str.strip()
            parts = cube_str.split(" ")

            if parts[1] == "red":
                self.red_cubes = int(parts[0])
            elif parts[1] == "green":
                self.green_cubes = int(parts[0])
            elif parts[1] == "blue":
                self.blue_cubes = int(parts[0])
            
class Game:
    def __init__(self, game_str: str):
        self.draws: list[Draw] = []

        parts = game_str.split(":")
        self.id = int(parts[0].split(" ")[1])

        draw_strs = parts[1].split(";")
        for draw_str in draw_strs:
            self.draws.append(Draw(draw_str))       
    

with open(args.filepath) as game_file:
    id_sum = 0
    power_sum = 0
    
    for line in game_file:
        game = Game(line)

        valid_game = True

        game_max_red_cubes = 0
        game_max_green_cubes = 0
        game_max_blue_cubes = 0

        for draw in game.draws:
            if draw.red_cubes > game_max_red_cubes: game_max_red_cubes = draw.red_cubes
            if draw.green_cubes > game_max_green_cubes: game_max_green_cubes = draw.green_cubes
            if draw.blue_cubes > game_max_blue_cubes: game_max_blue_cubes = draw.blue_cubes
            
        if game_max_red_cubes > MAX_RED_CUBES:
            valid_game = False
        elif game_max_green_cubes > MAX_GREEN_CUBES:
            valid_game = False
        elif game_max_blue_cubes > MAX_BLUE_CUBES:
            valid_game = False

        power_sum += game_max_red_cubes * game_max_green_cubes * game_max_blue_cubes

        if valid_game: 
            id_sum += game.id
        
    print(f"Sum of valid game id's is: {id_sum}")
    print(f"The sum of game powers is: {power_sum}")