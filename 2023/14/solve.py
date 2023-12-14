EXAMPLE = '''
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
'''

def parse(data):
    grid = data.strip().split('\n')
    walls = set()
    rocks = set()
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == 'O':
                rocks.add((x,y))
            elif c == '#':
                walls.add((x,y))
    grid_size = len(grid[0]), len(grid)
    return grid_size, walls, rocks

def move(rock, direction):
    x,y = rock
    dx,dy = direction
    return x+dx,y+dy

def inside_grid(grid_size, rock):
    x, y = rock
    w, h = grid_size
    return x >= 0 and x < w and y >= 0 and y < h

def sort_key(direction):
    dx,dy = direction
    if dx == 0:
        return lambda r:-r[1]*dy
    else:
        return lambda r:-r[0]*dx

def tilt(grid_size, walls, rocks, direction):
    rocks = set(rocks)
    for rock in sorted(rocks, key=sort_key(direction)):
        rocks.remove(rock)
        new_pos = move(rock, direction)
        while inside_grid(grid_size, new_pos) and new_pos not in walls and new_pos not in rocks:
            rock = new_pos
            new_pos = move(rock, direction)
        rocks.add(rock)
    return rocks

def cycle(grid_size, walls, rocks):
    for direction in [(0,-1), (-1, 0), (0,1), (1, 0)]:
        rocks = tilt(grid_size, walls, rocks, direction)
    return rocks

def calculate_load(grid_size, rocks):
    _, h = grid_size
    return sum(h-y for _,y in rocks)

def solve1(data):
    grid_size, walls, rocks = parse(data)
    rocks = tilt(grid_size, walls, rocks, (0, -1))
    return calculate_load(grid_size, rocks)

def print_board(grid_size, walls, rocks):
    w, h = grid_size
    for y in range(h):
        print(''.join('O' if (x,y) in rocks else '#' if (x,y) in walls else '.' for x in range(w)))

def solve2(data):
    grid_size, walls, rocks = parse(data)
    steps = []
    seen = set()
    while True:
        rocks = frozenset(cycle(grid_size, walls, rocks))
        if rocks in seen:
            previous_step = steps.index(rocks)
            cycle_length = len(steps) - previous_step
            #print(f'step {len(steps)} cycle length {cycle_length} load {calculate_load(grid_size, rocks)}')
            remaining = 1000000000 - 1 - len(steps)
            if remaining % cycle_length == 0:
                break
        seen.add(rocks)
        steps.append(rocks)
    return calculate_load(grid_size, rocks)

assert solve1(EXAMPLE) == 136
assert solve2(EXAMPLE) == 64

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
