from collections import defaultdict

SMALL_EXAMPLE = '''
AAAA
BBCD
BBCC
EEEC
'''

EXAMPLE = '''
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
'''

def parse(data):
    lines = data.strip().split('\n')
    plants = dict()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            plants[(x,y)] = c
    return plants

def adjacent(pos):
    x, y = pos
    return [
        (x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1),
    ]

def region_at(plants, pos):
    region = {pos}
    c = plants[pos]
    positions = [pos]
    while positions:
        new_positions = []
        for p in positions:
            for q in adjacent(p):
                if q in region or plants.get(q) != c:
                    continue
                region.add(q)
                new_positions.append(q)
        positions = new_positions
    return region

def all_regions(plants):
    remaining = dict(plants)
    regions = []
    while remaining:
        region = region_at(remaining, next(iter(remaining)))
        assert len(region) > 0
        regions.append(region)
        for pos in region:
            del remaining[pos]
    return regions

def perimiter_length(region):
    length = 0
    for p in region:
        length += sum(1 for q in adjacent(p) if q not in region)
    return length

def solve1(data):
    plants = parse(data)
    regions = all_regions(plants)
    total_price = 0
    for r in regions:
        total_price += len(r) * perimiter_length(r)
    return total_price

def perimiter_sides(region):
    left_fences = defaultdict(set)
    right_fences = defaultdict(set)
    up_fences = defaultdict(set)
    down_fences = defaultdict(set)
    for p in region:
        px, py = p
        for q in adjacent(p):
            if q in region:
                continue
            qx, qy = q
            x = min(px, qx)
            y = min(py, qy)
            if py == qy:
                fences = left_fences if qx < px else right_fences
                assert y not in fences[x]
                fences[x].add(y)
            else:
                assert px == qx
                fences = up_fences if qy < py else down_fences
                assert x not in fences[y]
                fences[y].add(x)
    sides = 0
    for fences in (left_fences, right_fences, up_fences, down_fences):
        for pieces in fences.values():
            prev = None
            for n in sorted(pieces):
                if n-1 != prev:
                    sides += 1
                prev = n
    return sides

def solve2(data):
    plants = parse(data)
    regions = all_regions(plants)
    total_price = 0
    for r in regions:
        total_price += len(r) * perimiter_sides(r)
    return total_price

assert solve1(SMALL_EXAMPLE) == 140
assert solve1(EXAMPLE) == 1930
assert solve2(SMALL_EXAMPLE) == 80
assert solve2(EXAMPLE) == 1206

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
