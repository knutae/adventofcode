EXAMPLE = '''
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
'''

EXAMPLE1 = '''
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
'''

EXAMPLE2 = '''
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
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

def within_grid(grid, pos):
    x, y = pos
    w, h = len(grid[0]), len(grid)
    return x >= 0 and x < w and y >= 0 and y < h

def fill_area(grid, loop, area):
    area = set(area)
    while True:
        added = 0
        for x, y in list(area):
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                pos = x + dx, y + dy
                if within_grid(grid, pos) and pos not in loop and pos not in area:
                    area.add(pos)
                    added += 1
        if added == 0:
            return area

def is_outside(grid, area):
    w, h = len(grid[0]), len(grid)
    return any(x == 0 or x == w-1 or y == 0 or y == h-1 for x, y in area)

def print_solution(grid, loop, inside, outside):
    for y, line in enumerate(grid):
        print(''.join('*' if (x,y) in loop else 'I' if (x,y) in inside else 'O' if (x,y) in outside else c for x, c in enumerate(line)))

def solve2(data):
    grid, start_pos = parse(data)
    # find all loop positions
    loop = {start_pos}
    current_positions = [start_pos]
    while True:
        new_positions = []
        for pos in current_positions:
            for new_pos in moves(grid, pos):
                if new_pos not in loop:
                    new_positions.append(new_pos)
                    loop.add(new_pos)
        if not new_positions:
            break
        current_positions = new_positions
    # traverse the loop in one direction and categorize adjacent "left" and "right" tiles
    left = set()
    right = set()
    pos = start_pos
    visited = {pos}
    finished = False
    while not finished:
        new_pos = None
        for p in moves(grid, pos):
            if p not in visited:
                new_pos = p
                break
        if new_pos is None:
            # should now be done traversing the loop
            # probably not important, but also include the final step back to the start pos
            assert visited == loop
            finished = True
            new_pos = start_pos
        visited.add(new_pos)
        ox, oy = pos
        nx, ny = new_pos
        dx, dy = nx - ox, ny - oy
        assert abs(dx+dy) == 1
        for x, y in (pos, new_pos):
            left_tile = x - dy, y + dx
            right_tile = x + dy, y - dx
            if within_grid(grid, left_tile) and left_tile not in loop:
                left.add(left_tile)
            if within_grid(grid, right_tile) and right_tile not in loop:
                right.add(right_tile)
        pos = new_pos
    # fill out left and right areas
    left = fill_area(grid, loop, left)
    right = fill_area(grid, loop, right)
    assert len(set.intersection(left, right)) == 0
    # detect which area is inside and outside
    if is_outside(grid, left):
        assert not is_outside(grid, right)
        inside, outside = right, left
    else:
        assert is_outside(grid, right)
        inside, outside = left, right
    #print_solution(grid, loop, inside, outside)
    grid_size = len(grid) * len(grid[0])
    assert len(inside) + len(outside) + len(loop) == grid_size
    return len(inside)

assert solve2(EXAMPLE1) == 8
assert solve2(EXAMPLE2) == 10

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
