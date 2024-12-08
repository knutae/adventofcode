from collections import defaultdict
from itertools import combinations

EXAMPLE = '''
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
'''

def parse(data):
    lines = data.strip().split('\n')
    height = len(lines)
    width = len(lines[0])
    antennas = defaultdict(set)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c != '.':
                antennas[c].add((x,y))
    return (width, height), dict(antennas)

def in_bounds(size, node):
    w, h = size
    x, y = node
    return x in range(w) and y in range(h)

def checked_add(size, antinodes, node):
    if in_bounds(size, node):
        antinodes.add(node)

def solve1(data):
    size, antennas = parse(data)
    antinodes = set()
    for antennas_list in antennas.values():
        for p, q in combinations(antennas_list, 2):
            px, py = p
            qx, qy = q
            dx = px - qx
            dy = py - qy
            checked_add(size, antinodes, (px + dx, py + dy))
            checked_add(size, antinodes, (qx - dx, qy - dy))
    return len(antinodes)

def solve2(data):
    size, antennas = parse(data)
    antinodes = set()
    for antennas_list in antennas.values():
        for p, q in combinations(antennas_list, 2):
            px, py = p
            qx, qy = q
            dx = px - qx
            dy = py - qy
            # pass 1
            x, y = p
            while in_bounds(size, (x, y)):
                antinodes.add((x, y))
                x += dx
                y += dy
            # pass 2
            x, y = p
            while in_bounds(size, (x, y)):
                antinodes.add((x, y))
                x -= dx
                y -= dy
    return len(antinodes)

assert solve1(EXAMPLE) == 14
assert solve2(EXAMPLE) == 34

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
