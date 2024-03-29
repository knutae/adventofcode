EXAMPLE = '''
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''

def parse_point(p):
    [x, y] = p.split(',')
    return int(x), int(y)

def parse_path(line):
    return [parse_point(p) for p in line.split(' -> ')]

def parse(input):
    return [parse_path(line) for line in input.strip().split('\n')]

def print_world(walls, sand):
    objects = set.union(walls, sand)
    xmin = min(p[0] for p in objects)
    xmax = max(p[0] for p in objects)
    ymin = min(p[1] for p in objects)
    ymax = max(p[1] for p in objects)
    for y in range(ymin, ymax + 1):
        print(''.join('#' if (x, y) in walls else 'o' if (x, y) in sand else ' ' for x in range(xmin, xmax+1)))

def step_sand(x, y, walls, sand, floor_y=None):
    if y+1 == floor_y:
        return x, y
    for p in [(x, y+1), (x-1, y+1), (x+1, y+1)]:
        if p not in walls and p not in sand:
            return p
    return x, y

def flow_sand(walls, sand, max_y=None, floor_y=None):
    p = 500, 0
    while True:
        px, py = p
        if max_y and py > max_y:
            return None
        new_p = step_sand(px, py, walls, sand, floor_y=floor_y)
        if p == new_p:
            return p
        p = new_p

def parse_walls(input):
    walls = set()
    for path in parse(input):
        for p1, p2 in zip(path, path[1:]):
            x1, y1 = p1
            x2, y2 = p2
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    walls.add((x1, y))
            else:
                assert y1 == y2
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    walls.add((x, y1))
    return walls

def solve1(input):
    walls = parse_walls(input)
    sand = set()
    max_y = max(p[1] for p in walls)
    while True:
        new_sand = flow_sand(walls, sand, max_y=max_y)
        if new_sand is None:
            break
        sand.add(new_sand)
    #print_world(walls, sand)
    return len(sand)

def solve2(input):
    walls = parse_walls(input)
    sand = set()
    floor_y = 2 + max(p[1] for p in walls)
    while (500, 0) not in sand:
        new_sand = flow_sand(walls, sand, floor_y=floor_y)
        sand.add(new_sand)
    #print_world(walls, sand)
    return len(sand)

assert solve1(EXAMPLE) == 24
assert solve2(EXAMPLE) == 93

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
