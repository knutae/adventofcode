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

def solve1(s):
    grid = parse(s)
    res = 0
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == '@' and count_adjacent(grid, x, y) < 4:
                res += 1
    #print(res)
    return res

assert solve1(EXAMPLE) == 13

with open('input') as f:
    s = f.read()

print(solve1(s))
