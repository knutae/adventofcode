EXAMPLE = '''
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
'''

def parse_coord(line):
    x, y = line.split(',')
    return int(x), int(y)

def parse_fold(line):
    assert line.startswith('fold along ')
    axis,n = line.split()[2].split('=')
    assert axis in ('x', 'y')
    return axis, int(n)

def parse(data):
    coords, folds = data.strip().split('\n\n')
    coords = [parse_coord(line) for line in coords.split('\n')]
    folds = [parse_fold(line) for line in folds.split('\n')]
    return coords, folds

def fold_x(coords, n):
    def fold_c(c):
        x, y = c
        x = n - (x-n) if x > n else x
        return x, y
    return {fold_c(c) for c in coords}

def fold_y(coords, n):
    def fold_c(c):
        x, y = c
        y = n - (y-n) if y > n else y
        return x, y
    return {fold_c(c) for c in coords}

def fold(coords, spec):
    axis, n = spec
    if axis == 'x':
        return fold_x(coords, n)
    if axis == 'y':
        return fold_y(coords, n)
    assert False

def solve1(data):
    coords, folds = parse(data)
    return len(fold(coords, folds[0]))

def print_coords(coords):
    min_x = min(c[0] for c in coords)
    max_x = max(c[0] for c in coords)
    min_y = min(c[1] for c in coords)
    max_y = max(c[1] for c in coords)
    for y in range(min_y, max_y + 1):
        print(''.join('#' if (x,y) in coords else ' ' for x in range(min_x, max_x + 1)))

def solve2(data):
    coords, folds = parse(data)
    for spec in folds:
        coords = fold(coords, spec)
    print_coords(coords)

assert solve1(EXAMPLE) == 17
#solve2(EXAMPLE)

with open('input') as f:
    puzzle_input = f.read()

print(solve1(puzzle_input))
solve2(puzzle_input)
