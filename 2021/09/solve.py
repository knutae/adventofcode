import math

EXAMPLE = '''
2199943210
3987894921
9856789892
8767896789
9899965678
'''

def parse(data):
    lines = data.strip().split('\n')
    return [[int(x) for x in line] for line in lines]

def adjacent(x, y, w, h):
    if x > 0:
        yield x-1, y
    if x < w-1:
        yield x+1, y
    if y > 0:
        yield x, y-1
    if y < h-1:
        yield x, y+1

def solve1(grid):
    risk_level_sum = 0
    h = len(grid)
    w = len(grid[0])
    for y, line in enumerate(grid):
        for x, n in enumerate(line):
            surrounding = [grid[y1][x1] for x1, y1 in adjacent(x, y, w, h)]
            if all(n < x for x in surrounding):
                #print(x, y, n, surrounding)
                risk_level_sum += 1 + n
    return risk_level_sum

def basin_size(grid, x, y):
    h = len(grid)
    w = len(grid[0])
    basin = {(x,y)}
    while True:
        size = len(basin)
        for x1, y1 in list(basin):
            for x2, y2 in adjacent(x1, y1, w, h):
                if (x2, y2) in basin or grid[y2][x2] == 9:
                    continue
                basin.add((x2, y2))
        if size == len(basin):
            break
    #print(basin)
    return len(basin)

def solve2(grid):
    basin_sizes = []
    h = len(grid)
    w = len(grid[0])
    for y, line in enumerate(grid):
        for x, n in enumerate(line):
            surrounding = [grid[y1][x1] for x1, y1 in adjacent(x, y, w, h)]
            if all(n < x for x in surrounding):
                #print(x, y, n, surrounding)
                basin_sizes.append(basin_size(grid, x, y))
    basin_sizes.sort(reverse=True)
    assert len(basin_sizes) >= 3
    return math.prod(basin_sizes[:3])

assert solve1(parse(EXAMPLE)) == 15
assert solve2(parse(EXAMPLE)) == 1134

with open('input') as f:
    grid = parse(f.read())

print(solve1(grid))
print(solve2(grid))
