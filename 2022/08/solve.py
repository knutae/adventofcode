TEST_INPUT = '''
30373
25512
65332
33549
35390
'''

def parse(input):
    lines = input.strip().split('\n')
    return [[int(x) for x in line] for line in lines]

def is_visible(grid, x, y):
    h = grid[y][x]
    return (
        all(grid[y][tx] < h for tx in range(x)) # left
        or all(grid[y][tx] < h for tx in range(x+1, len(grid[y]))) # right
        or all(grid[ty][x] < h for ty in range(y)) # up
        or all(grid[ty][x] < h for ty in range(y+1, len(grid))) # down
    )

def solve1(grid):
    return sum(1 for y in range(len(grid)) for x in range(len(grid[0])) if is_visible(grid, x, y))

assert solve1(parse(TEST_INPUT)) == 21

with open('input') as f:
    input = f.read()

print(solve1(parse(input)))
