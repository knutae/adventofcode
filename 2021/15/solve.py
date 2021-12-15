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

def step(grid, costs):
    updated = False
    for x0, y0 in dict(costs):
        c0 = costs[(x0, y0)]
        for x1, y1 in adjacent(grid, x0, y0):
            c1 = grid[y1][x1] + c0
            if (x1, y1) not in costs or c1 < costs[(x1, y1)]:
                costs[(x1, y1)] = c1
                updated = True
    return updated

def solve1(data):
    grid = parse(data)
    h = len(grid)
    w = len(grid[0])
    target = (w-1, h-1)
    costs = {(0,0): 0}
    while step(grid, costs):
        pass
    #print(costs)
    return costs[target]

assert solve1(EXAMPLE) == 40

with open('input') as f:
    puzzle_input = f.read()

print(solve1(puzzle_input))
