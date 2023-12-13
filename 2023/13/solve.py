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

def is_vertical_reflection(grid, row):
    h = len(grid)
    assert row >= 0 and row < h - 1
    a = row
    b = row + 1
    while a >= 0 and b < h:
        if grid[a] != grid[b]:
            return False
        a -= 1
        b += 1
    return True

def column(grid, i):
    return ''.join(row[i] for row in grid)

def is_horizontal_reflection(grid, col):
    w = len(grid[0])
    assert col >= 0 and col < w - 1
    a = col
    b = col + 1
    while a >= 0 and b < w:
        if column(grid, a) != column(grid, b):
            return False
        a -= 1
        b += 1
    return True

def solve_pattern(grid):
    vertical = [row+1 for row in range(len(grid) - 1) if is_vertical_reflection(grid, row)]
    horizonal = [col+1 for col in range(len(grid[0]) - 1) if is_horizontal_reflection(grid, col)]
    assert {len(vertical), len(horizonal)} == {0, 1}
    #print(horizonal, vertical)
    if vertical:
        return vertical[0] * 100
    else:
        return horizonal[0]

def solve1(data):
    patterns = parse(data)
    return sum(solve_pattern(grid) for grid in patterns)

assert solve1(EXAMPLE) == 405

with open('input') as f:
    data = f.read()

print(solve1(data))
