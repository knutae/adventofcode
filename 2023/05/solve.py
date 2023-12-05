from dataclasses import dataclass
from typing import List

EXAMPLE = '''
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''

@dataclass
class RangeMapping:
    dest_range_start: int
    source_range_start: int
    range_length: int

    def contains(self, source_value):
        return source_value in range(self.source_range_start, self.source_range_start + self.range_length)

    def convert(self, source_value):
        assert self.contains(source_value)
        return source_value - self.source_range_start + self.dest_range_start

@dataclass
class Map:
    mappings: List[RangeMapping]

    def convert(self, source_value):
        for mapping in self.mappings:
            if mapping.contains(source_value):
                return mapping.convert(source_value)
        return source_value

def parse_map(data):
    lines = data.strip().split('\n')
    mappings = [RangeMapping(*[int(n) for n in line.split()]) for line in lines[1:]]
    return Map(mappings)

def parse(data):
    [seeds, *maps] = data.strip().split('\n\n')
    seeds = [int(x) for x in seeds.split()[1:]]
    maps = [parse_map(m) for m in maps]
    return seeds, maps

def convert_seed_to_location(seed, maps):
    value = seed
    for m in maps:
        value = m.convert(value)
    return value

def solve1(data):
    seeds, maps = parse(data)
    return min(convert_seed_to_location(seed, maps) for seed in seeds)

assert solve1(EXAMPLE) == 35

with open('input') as f:
    data = f.read()

print(solve1(data))
