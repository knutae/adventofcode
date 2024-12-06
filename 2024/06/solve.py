from collections import defaultdict

EXAMPLE = '''
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
'''



def parse(data):
    lines = data.strip().split('\n')
    height = len(lines)
    width = len(lines[0])
    obstructions = set()
    guard = None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                obstructions.add((x,y))
            elif c == '^':
                assert guard == None
                guard = x,y
            else:
                assert c == '.'
    return (width, height), obstructions, guard

def turn_right(direction):
    dx, dy = direction
    return -dy, dx

assert turn_right((0, -1)) == (1, 0) # up -> right
assert turn_right((1, 0)) == (0, 1) # right -> down
assert turn_right((0, 1)) == (-1, 0) # down -> left
assert turn_right((-1, 0)) == (0, -1) # left -> up

def in_mapped_area(size, guard):
    w, h = size
    x, y = guard
    return x in range(w) and y in range(h)

def target_pos(guard, direction):
    x, y = guard
    dx, dy = direction
    return x+dx, y+dy

def solve1(data):
    size, obstructions, guard = parse(data)
    direction = (0, -1) # up
    visited = set()
    while in_mapped_area(size, guard):
        visited.add(guard)
        target = target_pos(guard, direction)
        if target in obstructions:
            direction = turn_right(direction)
        else:
            guard = target
    return len(visited)

assert solve1(EXAMPLE) == 41

def has_loop(size, obstructions, guard):
    direction = (0, -1) # up
    visited = defaultdict(list)
    while in_mapped_area(size, guard):
        if direction in visited[guard]:
            # have visited the same position while facing the same direction
            return True
        visited[guard].append(direction)
        target = target_pos(guard, direction)
        if target in obstructions:
            direction = turn_right(direction)
        else:
            guard = target
    # left the area, no loop
    return False

def solve2(data):
    size, obstructions, guard = parse(data)
    w, h = size
    loop_count = 0
    for y in range(h):
        for x in range(w):
            pos = x,y
            if pos == guard or pos in obstructions:
                continue
            if has_loop(size, obstructions | {pos}, guard):
                #print(f'loop at {pos}')
                loop_count += 1
    return loop_count

assert solve2(EXAMPLE) == 6

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
