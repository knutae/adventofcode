from collections import defaultdict

EXAMPLE = '''
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
'''

def parse_line(line):
    parts = line.split()
    return tuple([*[int(x) for x in parts[0].split(',')], *[int(x) for x in parts[2].split(',')]])

def parse(input):
    return [parse_line(line) for line in input.strip().split('\n')]

def solve1(input):
    points = parse(input)
    coords = defaultdict(int)
    for x1, y1, x2, y2 in points:
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2)+1):
                coords[(x1,y)] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2)+1):
                coords[(x,y1)] += 1
    #print(coords)
    result = len([p for p in coords.values() if p >= 2])
    return result

def solve2(input):
    points = parse(input)
    coords = defaultdict(int)
    for x1, y1, x2, y2 in points:
        dx = 1 if x2 > x1 else -1 if x2 < x1 else 0
        dy = 1 if y2 > y1 else -1 if y2 < y1 else 0
        x = x1
        y = y1
        coords[(x,y)] += 1
        while (x, y) != (x2, y2):
            x += dx
            y += dy
            coords[(x,y)] += 1
    #print(coords)
    result = len([p for p in coords.values() if p >= 2])
    #print(result)
    return result

assert solve1(EXAMPLE) == 5
assert solve2(EXAMPLE) == 12

with open('input') as f:
    puzzle_input = f.read()

print(solve1(puzzle_input))
print(solve2(puzzle_input))
