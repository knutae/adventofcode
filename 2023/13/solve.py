EXAMPLE = '''
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
'''

def parse_pattern(lines):
    grid = lines.split('\n')
    w = len(grid[0])
    assert all(len(row) == w for row in grid)
    return grid

def parse(input):
    patterns = input.strip().split('\n\n')
    return [parse_pattern(lines) for lines in patterns]

def count_diff(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)

def is_vertical_reflection(grid, row, smudges):
    h = len(grid)
    assert row >= 0 and row < h - 1
    a = row
    b = row + 1
    diff = 0
    while a >= 0 and b < h:
        diff += count_diff(grid[a], grid[b])
        if diff > smudges:
            return False
        a -= 1
        b += 1
    return diff == smudges

def column(grid, i):
    return ''.join(row[i] for row in grid)

def is_horizontal_reflection(grid, col, smudges):
    w = len(grid[0])
    assert col >= 0 and col < w - 1
    a = col
    b = col + 1
    diff = 0
    while a >= 0 and b < w:
        diff += count_diff(column(grid, a), column(grid, b))
        if diff > smudges:
            return False
        a -= 1
        b += 1
    return diff == smudges

def solve_pattern(grid, smudges):
    vertical = [row+1 for row in range(len(grid) - 1) if is_vertical_reflection(grid, row, smudges)]
    horizonal = [col+1 for col in range(len(grid[0]) - 1) if is_horizontal_reflection(grid, col, smudges)]
    assert {len(vertical), len(horizonal)} == {0, 1}
    #print(horizonal, vertical)
    if vertical:
        return vertical[0] * 100
    else:
        return horizonal[0]

def solve(data, smudges):
    patterns = parse(data)
    return sum(solve_pattern(grid, smudges) for grid in patterns)

def solve1(data):
    return solve(data, 0)

def solve2(data):
    return solve(data, 1)

assert solve1(EXAMPLE) == 405
assert solve2(EXAMPLE) == 400

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
