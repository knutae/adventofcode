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

def simplify_ranges(ranges):
    if len(ranges) == 0:
        return []
    ranges = list(sorted(ranges, key=lambda r: (r.start, r.stop)))
    result = [ranges[0]]
    for r in ranges[1:]:
        last = result[-1]
        if r.start > last.stop:
            result.append(r)
        else:
            result[-1] = range(last.start, max(r.stop, last.stop))
    return result

def exclude_one(r, exclude):
    if r.stop < exclude.start or r.start >= exclude.stop:
        return [r]
    result = []
    if r.start < exclude.start:
        result.append(range(r.start, exclude.start))
    if r.stop > exclude.stop:
        result.append(range(exclude.stop , r.stop))
    return result

def exclude_range(ranges, exclude):
    result = []
    for r in ranges:
        result.extend(exclude_one(r, exclude))
    return simplify_ranges(result)

@dataclass
class RangeMapping:
    dest_range_start: int
    source_range_start: int
    range_length: int

    def contains(self, source_value):
        return source_value in range(self.source_range_start, self.source_range_stop())

    def convert(self, source_value):
        assert self.contains(source_value)
        return source_value + self.offset()

    def source_range_stop(self):
        return self.source_range_start + self.range_length

    def offset(self):
        return self.dest_range_start - self.source_range_start

    def split_range(self, source_range):
        assert source_range.start < source_range.stop
        if source_range.stop <= self.source_range_start:
            return [], [source_range]
        if source_range.start >= self.source_range_stop():
            return [], [source_range]
        matched = range(max(source_range.start, self.source_range_start) + self.offset(),
                        min(source_range.stop, self.source_range_stop()) + self.offset())
        unmatched = []
        if source_range.start < self.source_range_start:
            unmatched.append(range(source_range.start, self.source_range_start))
        if source_range.stop > self.source_range_stop():
            unmatched.append(range(self.source_range_stop(), source_range.stop))
        unmatched = exclude_range(unmatched, matched)
        #print(self, " : ", source_range, "-->", result, "-->", simplify_ranges(result))
        return [matched], simplify_ranges(unmatched)

def test_range_mapping():
    r = RangeMapping(100, 20, 10)
    assert r.split_range(range(1, 20)) == ([], [range(1, 20)])
    assert r.split_range(range(30, 35)) == ([], [range(30, 35)])
    assert r.split_range(range(1, 23)) == ([range(100, 103)], [range(1, 20)])
    assert r.split_range(range(26, 35)) == ([range(106, 110)], [range(30, 35)])
    assert r.split_range(range(-100, 200)) == ([range(100, 110)], [range(-100, 20), range(30, 100), range(110, 200)])

test_range_mapping()

@dataclass
class Map:
    name: str
    mappings: List[RangeMapping]

    def convert(self, source_value):
        for mapping in self.mappings:
            if mapping.contains(source_value):
                return mapping.convert(source_value)
        return source_value

    def convert_range(self, source_range):
        all_matched = []
        remaining_unmatched = [source_range]
        for mapping in self.mappings:
            new_unmatched = []
            for r in remaining_unmatched:
                matched, unmatched = mapping.split_range(r)
                all_matched.extend(matched)
                new_unmatched.extend(unmatched)
            remaining_unmatched = simplify_ranges(new_unmatched)
            all_matched = simplify_ranges(all_matched)
        return simplify_ranges(all_matched + remaining_unmatched)

def parse_map(data):
    lines = data.strip().split('\n')
    name = lines[0].split()[0]
    mappings = [RangeMapping(*[int(n) for n in line.split()]) for line in lines[1:]]
    return Map(name, mappings)

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

def convert_seed_range_to_location_slow(seed_range, maps):
    return min(convert_seed_to_location(seed, maps) for seed in seed_range)

def solve2_slow(data):
    seeds, maps = parse(data)
    seed_ranges = [range(a, a+b) for a, b in zip(seeds[0::2], seeds[1::2])]
    return min(convert_seed_range_to_location_slow(seed_range, maps) for seed_range in seed_ranges)

def solve2(data):
    seeds, maps = parse(data)
    seed_ranges = [range(a, a+b) for a, b in zip(seeds[0::2], seeds[1::2])]
    value_ranges = simplify_ranges(seed_ranges)
    for m in maps:
        new_value_ranges = []
        for r in value_ranges:
            new_value_ranges.extend(m.convert_range(r))
        value_ranges = simplify_ranges(new_value_ranges)
        #print(m.name, value_ranges)
    return min(r.start for r in value_ranges)

assert solve1(EXAMPLE) == 35
assert solve2_slow(EXAMPLE) == 46
assert solve2(EXAMPLE) == 46

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
