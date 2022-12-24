from dataclasses import dataclass

EXAMPLE = '''
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
'''

@dataclass
class Valley:
    width: int
    height: int
    left: set[tuple[int, int]]
    right: set[tuple[int, int]]
    up: set[tuple[int, int]]
    down: set[tuple[int, int]]

def parse(input):
    lines = input.strip().split('\n')
    assert lines[0].startswith('#.#')
    assert lines[-1].endswith("#.#")
    state = Valley(
        height=len(lines) - 2,
        width=len(lines[1]) - 2,
        left=set(),
        right=set(),
        up=set(),
        down=set())
    for y, line in enumerate(lines[1:-1]):
        assert line.startswith('#') and line.endswith('#')
        for x, c in enumerate(line[1:-1]):
            pos = x, y
            if c == '<':
                state.left.add(pos)
            elif c == '>':
                state.right.add(pos)
            elif c == '^':
                state.up.add(pos)
            elif c == 'v':
                state.down.add(pos)
            else:
                assert c == '.'
    return state

def possible_moves(pos, width, height):
    x, y = pos
    yield x,y
    if y >= 0 and y < height:
        if x > 0:
            yield x-1, y
        if x < width - 1:
            yield x+1, y
    if y > 0:
        yield x, y-1
    if y < height - 1:
        yield x, y+1
    if x == width - 1 and y == height - 1:
        yield x, height
    if x == 0 and y == 0:
        yield 0, -1

def move_blizzards_horizontal(positions, dx, width):
    return {((x + dx) % width, y) for x,y in positions}

def move_blizzards_vertical(positions, dy, height):
    return {(x, (y + dy) % height) for x,y in positions}

def step_valley(valley):
    return Valley(
        width=valley.width,
        height=valley.height,
        left=move_blizzards_horizontal(valley.left, -1, valley.width),
        right=move_blizzards_horizontal(valley.right, 1, valley.width),
        up=move_blizzards_vertical(valley.up, -1, valley.height),
        down=move_blizzards_vertical(valley.down, 1, valley.height),
    )

def step_positions(positions, valley):
    new_positions = set()
    for pos in positions:
        for new_pos in possible_moves(pos, valley.width, valley.height):
            if new_pos in valley.left or new_pos in valley.right or new_pos in valley.up or new_pos in valley.down:
                continue
            new_positions.add(new_pos)
    return new_positions

def solve1(input):
    valley = parse(input)
    positions = {(0, -1)}
    target_pos = valley.width - 1, valley.height
    step = 0
    while target_pos not in positions:
        step += 1
        valley = step_valley(valley)
        positions = step_positions(positions, valley)
    return step

def solve2(input):
    valley = parse(input)
    start_pos = 0, -1
    target_pos = valley.width - 1, valley.height
    positions = {start_pos}
    step = 0
    while target_pos not in positions:
        step += 1
        valley = step_valley(valley)
        positions = step_positions(positions, valley)
    positions = {target_pos}
    while start_pos not in positions:
        step += 1
        valley = step_valley(valley)
        positions = step_positions(positions, valley)
    positions = {start_pos}
    while target_pos not in positions:
        step += 1
        valley = step_valley(valley)
        positions = step_positions(positions, valley)
    return step

assert solve1(EXAMPLE) == 18
assert solve2(EXAMPLE) == 54

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
