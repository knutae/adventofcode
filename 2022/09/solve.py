TEST_INPUT = '''
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''

DIRECTIONS = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, -1),
    'D': (0, 1),
}

def parse_line(line):
    [dir, n] = line.split()
    return DIRECTIONS[dir], int(n)

def parse(input):
    return [parse_line(line) for line in input.strip().split('\n')]

def cmp(a, b):
    return int(a > b) - int(a < b)

def move_head(head_pos, dir):
    return head_pos[0] + dir[0], head_pos[1] + dir[1]

def move_tail(tail_pos, head_pos):
    tx, ty = tail_pos
    hx, hy = head_pos
    if abs(tx - hx) <= 1 and abs(ty - hy) <= 1:
        # already touching, don't move
        return tail_pos
    else:
        return tx + cmp(hx, tx), ty + cmp(hy, ty)

def solve1(input):
    head_pos = (0,0)
    tail_pos = (0,0)
    tail_visited = {tail_pos}
    for dir, steps in parse(input):
        for _ in range(steps):
            head_pos = move_head(head_pos, dir)
            tail_pos = move_tail(tail_pos, head_pos)
            tail_visited.add(tail_pos)
    return len(tail_visited)

assert solve1(TEST_INPUT) == 13

with open('input') as f:
    input = f.read()

print(solve1(input))
