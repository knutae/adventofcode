EXAMPLE = '''
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
'''

def parse_path(line):
    path = []
    n = 0
    for c in line:
        if c.isdigit():
            n = 10 * n + int(c)
        else:
            if n > 0:
                path.append(n)
            n = 0
            path.append(c)
    if n > 0:
        path.append(n)
    return path

def parse(input):
    input = input.strip('\n')
    board, path = input.split('\n\n')
    board = board.split('\n')
    path = parse_path(path)
    return board, path

def column(board, x):
    return ''.join(row[x] if len(row) > x else ' ' for row in board)

def move(board, pos, direction):
    x, y = pos
    assert board[y][x] == '.'
    if direction in '<>':
        row = board[y]
        dx = 1 if direction == '>' else -1
        #print(repr(row), dx, x, len(row))
        while True:
            x = (x + dx) % len(row)
            if row[x] != ' ':
                break
    else:
        assert direction in '^v'
        col = column(board, x)
        dy = 1 if direction == 'v' else -1
        #print(repr(col), dy, y, len(col))
        while True:
            y = (y + dy) % len(col)
            if col[y] != ' ':
                break
    assert board[y][x] in '.#'
    if board[y][x] == '.':
        return x, y
    else:
        return pos

CLOCKWISE = {
    '>': 'v',
    'v': '<',
    '<': '^',
    '^': '>',
}

COUNTER_CLOCKWISE = {
    '>': '^',
    '^': '<',
    '<': 'v',
    'v': '>',
}

def turn(direction, turn):
    assert turn in 'LR'
    if turn == 'R':
        return CLOCKWISE[direction]
    else:
        return COUNTER_CLOCKWISE[direction]

def solve1(input):
    board, path = parse(input)
    pos = board[0].index('.'), 0
    direction = '>'
    for p in path:
        if isinstance(p, str):
            old_direction = direction
            direction = turn(direction, p)
            #print(f'Turned {p}: {old_direction} -> {direction}')
        else:
            old_pos = pos
            for _ in range(p):
                pos = move(board, pos, direction)
            #print(f'Moved {p}, {old_pos} -> {pos}')
    #print(pos, direction)
    col, row = pos
    return 1000 * (row + 1) + 4 * (col + 1) + '>v<^'.index(direction)

def rotate_left_2d(x, y):
    assert (x == 0 or y == 0) and abs(x + y) == 1
    return -y, x

def rotate_right_2d(x, y):
    assert (x == 0 or y == 0) and abs(x + y) == 1
    return y, -x

def rotate_2d(x, y, left):
    if left:
        return rotate_left_2d(x, y)
    else:
        return rotate_right_2d(x, y)

assert rotate_left_2d(1, 0) == (0, 1)
assert rotate_left_2d(0, 1) == (-1, 0)
assert rotate_left_2d(-1, 0) == (0, -1)
assert rotate_left_2d(0, -1) == (1, 0)
assert rotate_right_2d(1, 0) == (0, -1)
assert rotate_right_2d(0, 1) == (1, 0)
assert rotate_right_2d(-1, 0) == (0, 1)
assert rotate_right_2d(0, -1) == (-1, 0)

def rotate_left_3d(vec, around):
    x, y, z = vec
    nx, ny, nz = around
    if nx != 0:
        assert x == 0
        y, z = rotate_2d(y, z, nx > 0)
    elif ny != 0:
        assert y == 0
        x, z = rotate_2d(x, z, ny > 0)
    else:
        assert nz != 0 and z == 0
        x, y = rotate_2d(x, y, nz > 0)
    return x, y, z

def rotate_right_3d(vec, around):
    x, y, z = vec
    nx, ny, nz = around
    if nx != 0:
        assert x == 0
        y, z = rotate_2d(y, z, nx < 0)
    elif ny != 0:
        assert y == 0
        x, z = rotate_2d(x, z, ny < 0)
    else:
        assert nz != 0 and z == 0
        x, y = rotate_2d(x, y, nz < 0)
    return x, y, z

class CubeFace:
    def __init__(self, normal, forward):
        self.normal = normal # perpendicular vector
        self.forward = forward # "up" vector on board

    def left(self):
        return CubeFace(rotate_left_3d(self.normal, self.forward), self.forward)
    
    def right(self):
        return CubeFace(rotate_right_3d(self.normal, self.forward), self.forward)
    
    def down(self):
        right = rotate_left_3d(self.forward, self.normal)
        return CubeFace(rotate_left_3d(self.normal, right), rotate_left_3d(self.normal, right))

assert solve1(EXAMPLE) == 6032

with open('input') as f:
    input = f.read()

print(solve1(input))
