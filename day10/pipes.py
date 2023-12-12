# Advent of code day 10

import argparse
from enum import Enum
from pathlib import Path
import sys
from typing import Optional

parser = argparse.ArgumentParser(description="Find the animal")
parser.add_argument('filepath', type=Path, help="Pipe file.")

args = parser.parse_args()

class Face(Enum):
    Top = 1
    Bottom = 2
    Left = 3
    Right = 4
    End = 5
    
class Pipe:
    def __init__(self, pipe_char: str, is_origional = False):
        self.char = pipe_char 
        self.face_map: dict[Face, Face] = {}

        self.is_origional = is_origional

        if pipe_char == "|": self._add_map(Face.Top, Face.Bottom)
        elif pipe_char == "-": self._add_map(Face.Left, Face.Right)
        elif pipe_char == "L": self._add_map(Face.Top, Face.Right)
        elif pipe_char == "J": self._add_map(Face.Top, Face.Left)
        elif pipe_char == "7": self._add_map(Face.Bottom, Face.Left)
        elif pipe_char == "F": self._add_map(Face.Bottom, Face.Right)

    def map_face(self, in_face: Face) -> Face:
        return self.face_map.get(in_face, Face.End)

    def _add_map(self, dir1: Face, dir2: Face):
        self.face_map[dir1] = dir2
        self.face_map[dir2] = dir1

pipes: list[list[Pipe]] = []

def find_loop(start_pos: tuple[int, int], start_face: Face) -> Optional[list[tuple[int, int]]]:
    count = 0
    current_face = start_face

    current_x = start_pos[0]
    current_y = start_pos[1]

    visited: set[int] = set()

    while current_face != Face.End and (current_x >= 0 or current_x < len(pipes[0]) or current_y >= 0 or current_y < len(pipes)):
        visited.add(current_y * len(pipes[0]) + current_x)
        
        # Convert to the face and position of next pipe
        if current_face == Face.Top:
            current_y -= 1
            current_face = Face.Bottom
        elif current_face == Face.Bottom:
            current_y += 1
            current_face = Face.Top
        elif current_face == Face.Left:
            current_x -= 1
            current_face = Face.Right
        elif current_face == Face.Right:
            current_x += 1
            current_face = Face.Left
        else:
            raise Exception("Invalid face.")
        
        count += 1

        if current_x == start_pos[0] and current_y == start_pos[1]:
            return visited
        
        current_face = pipes[current_y][current_x].map_face(current_face)

    return None

def mark_non_enclosed(seed_pos: tuple[int, int]):    
    if pipes[seed_pos[1]][seed_pos[0]].char == ".":
        pipes[seed_pos[1]][seed_pos[0]].char = "X"
    
    for x in range(seed_pos[0] - 1, seed_pos[0] + 2):
        for y in range(seed_pos[1] - 1, seed_pos[1] + 2):
            if x != seed_pos[0] or y != seed_pos[0]:
                if x >= 0 and x < len(pipes[0]) and y >= 0 and y < len(pipes):
                    if pipes[y][x].char == ".":
                        mark_non_enclosed((x, y))

def dump_map():
    with open("out.txt", "w") as pipe_file:
        for i in range(len(pipes)):
            for j in range(len(pipes[i])):
                pipe_file.write(pipes[i][j].char)
            pipe_file.write("\n")

start_x = 0
start_y = 0
with open(args.filepath) as pipe_file:
    for y, line in enumerate(pipe_file):
        line = line.strip()

        if y == 0:
            pipes.append([Pipe(".")] * 2 * (len(line) + 1))
        
        s_pos = line.rfind("S")
        if s_pos > -1: 
            start_x = s_pos * 2 + 1
            start_y = y * 2 + 1
        
        this_line: list[Pipe] = []
        insert_line: list[Pipe] = []
        this_line.append(Pipe("."))
        insert_line.append(Pipe("*"))
        for char in line:
            this_line.append(Pipe(char, True))
            
            # Make the gaps between pipes into actual gaps by extending characters
            this_line.append(Pipe("-") if char in ["S", "-", "F", "L"] else Pipe("."))

            insert_line.append(Pipe("|") if this_line[-2].char in ["S", "|", "F", "7"] else Pipe("."))
            insert_line.append(Pipe("|") if this_line[-1].char in ["S", "|", "F", "7"] else Pipe("."))
        this_line.append(Pipe("."))
        insert_line.append(Pipe("."))
        
        pipes.append(this_line)
        pipes.append(insert_line)
    
    pipes.append([Pipe(".")] * 2 * (len(line) + 1))

visited = [path for path in [find_loop((start_x, start_y), face) for face in [Face.Top, Face.Bottom, Face.Left, Face.Right]] if path][0]

midpoint = int(len(visited) / 4)
print(f"Midpoint (Part 1): {midpoint}")

for y in range(len(pipes)):
    for x in range(len(pipes[0])):
        if y * len(pipes[0]) + x not in visited:
            pipes[y][x].char = "."

sys.setrecursionlimit(len(pipes[0]) * len(pipes))
mark_non_enclosed((0,0))

enclosed_count = 0
for y in range(len(pipes)):
    for x in range(len(pipes[0])):
        if pipes[y][x].char == "." and pipes[y][x].is_origional: enclosed_count += 1

print(f"Enclosed count (Part 2): {enclosed_count}")
