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

def parse_line(line):
    direction, length, color = line.split()
    length = int(length)
    color = color[1:-1]
    return direction, length, color

def parse(data):
    lines = data.strip().split('\n')
    return [parse_line(line) for line in lines]

DIRECTIONS = {
    'R': (1,0),
    'D': (0,1),
    'L': (-1,0),
    'U': (0,-1),
}

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

def solve1(data):
    dig_plan = parse(data)
    x, y = 0, 0
    #tiles = {(x,y)}
    tiles = set()
    for direction, length, _ in dig_plan:
        dx, dy = DIRECTIONS[direction]
        for _ in range(length):
            x += dx
            y += dy
            assert (x,y) not in tiles
            tiles.add((x,y))
    tiles = fill_tiles(tiles)
    #print_grid(tiles)
    return len(tiles)

assert solve1(EXAMPLE) == 62

with open('input') as f:
    data = f.read()

print(solve1(data))
