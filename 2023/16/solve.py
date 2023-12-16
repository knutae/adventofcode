
EXAMPLE = r'''
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
'''

def parse(data):
    grid = data.strip().split('\n')
    tiles = dict()
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c != '.':
                tiles[(x,y)] = c
    dimensions = len(grid[0]), len(grid)
    return dimensions, tiles

#print(parse(EXAMPLE))

def handle_mirror(direction, mirror):
    x, y = direction
    assert abs(x+y) == 1
    if mirror == '/':
        return -y, -x
    if mirror == '\\':
        return y, x
    assert False

def handle_splitter(direction, splitter):
    x, y = direction
    assert abs(x+y) == 1
    if splitter == '-':
        if y == 0:
            return [direction]
        else:
            return [(-1, 0), (1, 0)]
    if splitter == '|':
        if x == 0:
            return [direction]
        else:
            return [(0, -1), (0, 1)]
    assert False

def handle_tile(direction, tile):
    if tile in '/\\':
        return [handle_mirror(direction, tile)]
    if tile in '-|':
        return handle_splitter(direction, tile)
    assert False

def move_beam(beam, dimensions, tiles):
    w, h = dimensions
    position, direction = beam
    new_position = tuple(a+b for a, b in zip(position, direction))
    x, y = new_position
    if x < 0 or x >= w or y < 0 or y >= h:
        # moved outside grid
        return []
    if new_position in tiles:
        return [(new_position, new_direction) for new_direction in handle_tile(direction, tiles[new_position])]
    else:
        return [(new_position, direction)]

def print_grid(dimensions, tiles, beams_visited):
    pos_visited = {pos for pos,_ in beams_visited}
    w, h = dimensions
    for y in range(h):
        print(''.join('#' if (x,y) in pos_visited else tiles.get((x,y), '.') for x in range(w)))

def solve1(data):
    dimensions, tiles = parse(data)
    active_beams = [((-1,0), (1,0))]
    beams_visited = set()
    while active_beams:
        new_beams = []
        for beam in active_beams:
            new_beams.extend(b for b in move_beam(beam, dimensions, tiles) if b not in beams_visited)
        active_beams = new_beams
        beams_visited.update(active_beams)
    #print_grid(dimensions, tiles, beams_visited)
    return len({pos for pos,_ in beams_visited})

assert solve1(EXAMPLE) == 46

with open('input') as f:
    data = f.read()

print(solve1(data))
