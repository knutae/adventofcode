EXAMPLE = '''
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
'''

DIRECTIONS = {
    'R': (1,0),
    'D': (0,1),
    'L': (-1,0),
    'U': (0,-1),
}

def parse_line(line, v2):
    direction, length, color = line.split()
    length = int(length)
    if v2:
        color = color[2:-1]
        length = int(color[:-1], 16)
        direction = 'RDLU'[int(color[-1])]
    direction = DIRECTIONS[direction]
    return direction, length

def parse(data, v2=False):
    lines = data.strip().split('\n')
    return [parse_line(line, v2) for line in lines]

def print_grid(tiles):
    y1 = min(y for _,y in tiles)
    y2 = max(y for _,y in tiles)+1
    x1 = min(x for x,_ in tiles)
    x2 = max(x for x,_ in tiles)+1
    for y in range(y1,y2):
        print(''.join('#' if (x,y) in tiles else '.' for x in range(x1,x2)))

def neighbours(tile):
    x,y = tile
    yield x-1,y
    yield x+1,y
    yield x,y-1
    yield x,y+1

def fill_tiles(tiles):
    y = min(y for _,y in tiles)
    x1 = min(x for x,_ in tiles)
    x2 = max(x for x,_ in tiles)+1
    start_tile = None
    for x in range(x1, x2):
        if (x,y) in tiles and (x,y+1) not in tiles:
            start_tile = x, y+1
            break
    assert start_tile
    filled = set(tiles)
    filled.add(start_tile)
    current_tiles = [start_tile]
    while current_tiles:
        new_tiles = []
        for old_tile in current_tiles:
            for tile in neighbours(old_tile):
                if tile not in filled:
                    filled.add(tile)
                    new_tiles.append(tile)
        current_tiles = new_tiles
    return filled

def solve_simple(dig_plan):
    tiles = set()
    x, y = 0, 0
    for direction, length in dig_plan:
        dx, dy = direction
        for _ in range(length):
            x += dx
            y += dy
            assert (x,y) not in tiles
            tiles.add((x,y))
    return fill_tiles(tiles)

def solve1(data):
    dig_plan = parse(data)
    tiles = solve_simple(dig_plan)
    return len(tiles)

def plan_to_path(dig_plan):
    x, y = 0, 0
    path = [(0,0)]
    for direction, length in dig_plan:
        dx, dy = direction
        x += dx * length
        y += dy * length
        path.append((x,y))
    assert x == 0 and y == 0
    return path

def sign(n):
    return n and [1,-1][n<0]

def solve2(data):
    dig_plan = parse(data, v2=True)
    path = plan_to_path(dig_plan)
    x_index = [*sorted({x for x,_ in path})]
    y_index = [*sorted({y for _,y in path})]
    index_dig_plan = []
    for p2, p1 in zip(path[1:] + path[:1], path):
        x1, y1 = p1
        x2, y2 = p2
        x1 = x_index.index(x1)
        x2 = x_index.index(x2)
        y1 = y_index.index(y1)
        y2 = y_index.index(y2)
        dx = x2 - x1
        dy = y2 - y1
        length = max(abs(dx), abs(dy)) * 2
        direction = sign(dx), sign(dy)
        index_dig_plan.append((direction, length))
    index_tiles = solve_simple(index_dig_plan)
    min_xi = min(x for x,_ in index_tiles)
    min_yi = min(y for _,y in index_tiles)
    index_tiles = {(xi-min_xi, yi-min_yi) for xi, yi in index_tiles}
    result = 0
    for xi, yi in index_tiles:
        assert xi >= 0
        assert yi >= 0
        # even indexes are vertices, odd are ranges
        if xi % 2 == 0:
            w = 1
        else:
            w = x_index[xi//2 + 1] - x_index[xi//2] - 1
        if yi % 2 == 0:
            h = 1
        else:
            h = y_index[yi//2 + 1] - y_index[yi//2] - 1
        result += w*h
    return result

assert solve1(EXAMPLE) == 62
assert solve2(EXAMPLE) == 952408144115

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
