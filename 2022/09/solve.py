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

LARGER_TEST_INPUT = '''
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
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

def solve2(input):
    rope = [(0,0) for _ in range(10)]
    tail_visited = {(0,0)}
    for dir, steps in parse(input):
        for _ in range(steps):
            new_rope = [move_head(rope[0], dir)]
            for pos in rope[1:]:
                new_rope.append(move_tail(pos, new_rope[-1]))
            rope = new_rope
            assert len(rope) == 10
            tail_visited.add(rope[-1])
    return len(tail_visited)

assert solve1(TEST_INPUT) == 13
assert solve2(TEST_INPUT) == 1
assert solve2(LARGER_TEST_INPUT) == 36

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
