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

assert solve1(EXAMPLE) == 6032

with open('input') as f:
    input = f.read()

print(solve1(input))
