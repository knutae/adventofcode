EXAMPLE = '''
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
'''

def parse(data):
    lines = data.strip().split('\n')
    return [[int(c) for c in line] for line in lines]

def adjacent(grid, x, y):
    h = len(grid)
    w = len(grid[0])
    if y > 0:
        yield x, y-1
    if x > 0:
        yield x-1, y
    if x < w-1:
        yield x+1, y
    if y < h-1:
        yield x, y+1

def step(grid, costs, last_updated):
    new_updated = []
    for x0, y0 in last_updated:
        c0 = costs[(x0, y0)]
        for x1, y1 in adjacent(grid, x0, y0):
            c1 = grid[y1][x1] + c0
            if (x1, y1) not in costs or c1 < costs[(x1, y1)]:
                costs[(x1, y1)] = c1
                new_updated.append((x1, y1))
    return new_updated

def solve_grid(grid):
    h = len(grid)
    w = len(grid[0])
    target = (w-1, h-1)
    costs = {(0,0): 0}
    last_updated = [(0,0)]
    while last_updated:
        last_updated = step(grid, costs, last_updated)
    #print(costs)
    return costs[target]

def solve1(data):
    return solve_grid(parse(data))

assert solve1(EXAMPLE) == 40

def inc(n, i):
    return 1+(n+i-1)%9

assert inc(9, 0) == 9
assert inc(9, 1) == 1
assert inc(5, 6) == 2

def extend_grid(grid):
    h = len(grid)
    w = len(grid[0])
    new_grid = []
    for y in range(h*5):
        line = []
        ydiv = y // h
        ymod = y % h
        for x in range(w*5):
            xdiv = x // w
            xmod = x % w
            line.append(inc(grid[ymod][xmod], xdiv + ydiv))
        new_grid.append(line)
    return new_grid

def solve2(data):
    grid = extend_grid(parse(data))
    return solve_grid(grid)

assert solve2(EXAMPLE) == 315

with open('input') as f:
    puzzle_input = f.read()

print(solve1(puzzle_input))
print(solve2(puzzle_input))
