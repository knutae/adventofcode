EXAMPLE = '''
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
'''

def parse(data):
    data = data.strip()
    start_pos = data.index('S')
    lines = data.split('\n')
    w = len(lines[0]) + 1
    x, y = start_pos % w, start_pos // w
    assert lines[y][x] == 'S'
    return lines, (x, y)

def moves(grid, pos):
    w, h = len(grid[0]), len(grid)
    x, y = pos
    c = grid[y][x]
    # left
    if x >= 0 and c in 'S-7J' and grid[y][x-1] in '-LF':
        yield x-1, y
    # right
    if x < w and c in 'S-LF' and grid[y][x+1] in '-7J':
        yield x+1, y
    # up
    if y >= 0 and c in 'S|LJ' and grid[y-1][x] in '|7F':
        yield x, y-1
    # down
    if y < h and c in 'S|7F' and grid[y+1][x] in '|LJ':
        yield x, y+1

def solve1(data):
    grid, start_pos = parse(data)
    visited = {start_pos}
    current_positions = [start_pos]
    distance = 0
    while True:
        new_positions = []
        for pos in current_positions:
            for new_pos in moves(grid, pos):
                if new_pos not in visited:
                    new_positions.append(new_pos)
                    visited.add(new_pos)
        #print(distance, new_positions)
        if not new_positions:
            break
        current_positions = new_positions
        distance += 1
    #print(distance, current_positions)
    return distance

assert solve1(EXAMPLE) == 8

with open('input') as f:
    data = f.read()

print(solve1(data))
