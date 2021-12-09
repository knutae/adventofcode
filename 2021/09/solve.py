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

def solve1(grid):
    risk_level_sum = 0
    h = len(grid)
    w = len(grid[0])
    for y, line in enumerate(grid):
        for x, n in enumerate(line):
            surrounding = []
            if x > 0:
                surrounding.append(line[x-1])
            if x < w-1:
                surrounding.append(line[x+1])
            if y > 0:
                surrounding.append(grid[y-1][x])
            if y < h-1:
                surrounding.append(grid[y+1][x])
            if all(n < x for x in surrounding):
                #print(x, y, n, surrounding)
                risk_level_sum += 1 + n
    return risk_level_sum

assert solve1(parse(EXAMPLE)) == 15

with open('input') as f:
    grid = parse(f.read())

print(solve1(grid))
