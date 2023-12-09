# Advent of code day 5

import argparse
from io import TextIOWrapper
import math
from pathlib import Path
from typing import Optional, Type
from dataclasses import dataclass, field

parser = argparse.ArgumentParser(description="Help with gardening.")
parser.add_argument('filepath', type=Path, help="Almanac file.")

args = parser.parse_args()

class Range:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def contains_val(self, val: int) -> bool:
        if val >= self.start and val < self.end: return True
        return False
            
    def get_range_overlap(self, range: Type["Range"]) -> Type["RangeOverlap"]:

        if range.start >= self.end or range.end <= self.start:
            # Cases where there is no overlap
            return RangeOverlap(None, [range])
        covered_range = Range(max(range.start, self.start), min(range.end, self.end))
        uncovered_ranges = []

        if range.start < covered_range.start:
            uncovered_ranges.append(Range(range.start, self.start))
        if range.end > covered_range.end:
            uncovered_ranges.append(Range(self.end, range.end))

        return RangeOverlap(covered_range, uncovered_ranges)

@dataclass
class RangeOverlap:
    covered_range: Optional[Range] = None
    uncovered_ranges: list[Range] = field(default_factory=list)

class MapRange(Range):
    def __init__(self, start, end, dest_start):
        super().__init__(start, end)
        self.dest_start = dest_start
        self.offset = dest_start - start
    
    @classmethod
    def from_str(cls, range_str: str) -> Type["MapRange"]:
        range_str = range_str.strip()
        vals = [int(val_str) for val_str in range_str.split(" ")]
        return cls(vals[1], vals[1] + vals[2], vals[0])
        
    def get_dest_val(self, src: int) -> int:
        if not self.contains_val(src):
            return -1
        else:
            return self.dest_start + (src - self.start)
    
class Mapping:
    def __init__(self, map_from: str, map_to: str):
        self.map_from = map_from
        self.map_to = map_to

        self.map_ranges: list[MapRange] = []

    @classmethod
    def from_file(cls, file_obj: TextIOWrapper) -> Type["Mapping"]:
        # Read the first line 
        map_parts = file_obj.readline().split(" ")[0].split("-to-")
        mapping = Mapping(map_parts[0], map_parts[1])

        while True:
            line = file_obj.readline().strip()
            if not line: break

            mapping.add_range(line)
        
        return mapping

    def add_range(self, range_str: str):
        self.map_ranges.append(MapRange.from_str(range_str))

    def get_mapped_val(self, src: int) -> int:
        for range in self.map_ranges:
            dest = range.get_dest_val(src)
            if dest > 0: return dest

        return src
    
    def get_ranges(self, ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:

        new_ranges: list[tuple[int, int]] = []
        
        for t_range in ranges:
            remaining_ranges = [t_range]
            for map_range in self.map_ranges:
                for _ in range(len(remaining_ranges)):
                    range_overlap = map_range.get_range_overlap(remaining_ranges.pop(0))
                    remaining_ranges += range_overlap.uncovered_ranges
                    
                    if range_overlap.covered_range:
                        new_ranges.append(Range(range_overlap.covered_range.start + map_range.offset, range_overlap.covered_range.end + map_range.offset))
            
            new_ranges += remaining_ranges

        return new_ranges
    
class Almanac:
    def __init__(self):
        self.mappings: dict[str, Mapping] = {}

    @classmethod
    def from_file(cls, file_obj: TextIOWrapper) -> Type["Almanac"]:
        almanac = Almanac()

        while True:
            file_pos = file_obj.tell()
            if file_obj.readline().strip():
                file_obj.seek(file_pos)
                mapping = Mapping.from_file(file_obj)
                almanac.mappings[mapping.map_from] = mapping
            else:
                return almanac

    def map_value(self, value: int, from_type: str, to_type: str) -> int:

        current_map = self.mappings.get(from_type) 

        if not current_map:
            raise Exception(f"Almanac contains no mapping from {from_type}.")          
        
        new_val = current_map.get_mapped_val(value)

        if to_type == current_map.map_to:
            return new_val

        return self.map_value(new_val, current_map.map_to, to_type)
    
    def map_ranges(self, ranges: list[Range], from_type: str, to_type: str) -> list[Range]:

        current_map = self.mappings.get(from_type) 

        if not current_map:
            raise Exception(f"Almanac contains no mapping from {from_type}.")          
        
        new_ranges = current_map.get_ranges(ranges)

        if to_type == current_map.map_to:
            return new_ranges

        return self.map_ranges(new_ranges, current_map.map_to, to_type)


with open(args.filepath) as almanc_file:
    # Read the seed line
    seeds = [int(seed_no) for seed_no in almanc_file.readline().split(":")[1].strip().split(" ")]

    almanc_file.readline() # Skip next line to get to mapping

    almanac = Almanac.from_file(almanc_file)

    min_location = math.inf

    for i in range(len(seeds)):
        location_no = almanac.map_value(seeds[i], "seed", "location")
        if location_no < min_location:
            min_location = location_no

    print(f"Min location no for Part 1 is: {min_location}")

    ranges: list[Range] = []

    for i in range(0, len(seeds), 2):
        new_ranges = almanac.map_ranges([Range(seeds[i], seeds[i] + seeds[i+1])], "seed", "location")
        ranges += new_ranges

    min_location= min([range.start for range in ranges])

    print(f"Min location for Part 2 is: {min_location}")



    


