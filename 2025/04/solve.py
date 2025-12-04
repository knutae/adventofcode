EXAMPLE = '''
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
'''

def parse(s):
    return s.strip().split('\n')

def within_grid(grid, x, y):
    w, h = len(grid[0]), len(grid)
    return x >= 0 and x < w and y >= 0 and y < h

def adjacent(grid, x, y):
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            xx = x + dx
            yy = y + dy
            if (dx,dy) != (0,0) and within_grid(grid, xx, yy):
                #print(x, y, xx, yy)
                yield xx, yy

def count_adjacent(grid, x, y):
    return sum(1 for xx, yy in adjacent(grid, x, y) if grid[yy][xx] == '@')

def removable_coords(grid):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == '@' and count_adjacent(grid, x, y) < 4:
                yield x, y

def solve1(s):
    grid = parse(s)
    return sum(1 for _ in removable_coords(grid))

assert solve1(EXAMPLE) == 13

def remove_from_grid(grid, coords):
    return [
        ''.join('.' if (x,y) in coords else c for x, c in enumerate(row))
        for y, row in enumerate(grid)
    ]

def solve2(s):
    grid = parse(s)
    total_removed = 0
    while True:
        coords = set(removable_coords(grid))
        if len(coords) == 0:
            break
        total_removed += len(coords)
        grid = remove_from_grid(grid, coords)
    return total_removed

assert solve2(EXAMPLE) == 43

with open('input') as f:
    s = f.read()

print(solve1(s))
print(solve2(s))
