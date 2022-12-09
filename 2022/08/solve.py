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

def viewing_distance(grid, x, y, dx, dy):
    h = grid[y][x]
    tx = x + dx
    ty = y + dy
    distance = 0
    while tx >= 0 and tx < len(grid[0]) and ty >= 0 and ty < len(grid):
        distance += 1
        if grid[ty][tx] >= h:
            break
        tx += dx
        ty += dy
    return distance

def scenic_score(grid, x, y):
    return (
        viewing_distance(grid, x, y, -1, 0) *
        viewing_distance(grid, x, y, 1, 0) *
        viewing_distance(grid, x, y, 0, -1) *
        viewing_distance(grid, x, y, 0, 1)
    )

def solve2(grid):
    return max(scenic_score(grid, x, y) for y in range(len(grid)) for x in range(len(grid[0])))

test_input = parse(TEST_INPUT)
assert solve1(test_input) == 21
assert viewing_distance(test_input, 2, 1, 0, -1) == 1
assert viewing_distance(test_input, 2, 1, -1, 0) == 1
assert viewing_distance(test_input, 2, 1, 1, 0) == 2
assert viewing_distance(test_input, 2, 1, 0, 1) == 2
assert scenic_score(test_input, 2, 1) == 4
assert solve2(test_input) == 8

with open('input') as f:
    input = f.read()

print(solve1(parse(input)))
print(solve2(parse(input)))
