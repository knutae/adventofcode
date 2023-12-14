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

def tilt_north(walls, rocks):
    rocks = set(rocks)
    for rock in sorted(rocks, key=lambda r:r[1]):
        rocks.remove(rock)
        x,y = rock
        while y > 0 and (x,y-1) not in walls and (x,y-1) not in rocks:
            y -= 1
        rocks.add((x,y))
    return rocks

def calculate_load(grid_size, rocks):
    _, h = grid_size
    return sum(h-y for _,y in rocks)

def solve1(data):
    grid_size, walls, rocks = parse(data)
    rocks = tilt_north(walls, rocks)
    return calculate_load(grid_size, rocks)

assert solve1(EXAMPLE) == 136

with open('input') as f:
    data = f.read()

print(solve1(data))
