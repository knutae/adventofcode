from collections import Counter

EXAMPLE = '''
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
'''

def parse(input):
    positions = set()
    for y, line in enumerate(input.strip().split('\n')):
        for x, c in enumerate(line):
            if c == '#':
                positions.add((x,y))
            else:
                assert c == '.'
    return positions

def print_rectangle(positions):
    for y in range(min(y for _,y in positions), 1+max(y for _,y in positions)):
        print(''.join('#' if (x,y) in positions else '.'for x in range(
            min(x for x,_ in positions),
            1+max(x for x,_ in positions))))

def surrounding_positions(pos):
    px, py = pos
    for x in range(px-1, px+2):
        for y in range(py-1, py+2):
            if (x, y) != pos:
                yield x, y

def positions_in_direction(pos, move):
    px, py = pos
    mx, my = move
    if mx == 0:
        # vertical direction
        y = py + my
        for dx in (-1, 0, 1):
            yield px + dx, y
    else:
        assert my == 0
        # horizontal direction
        x = px + mx
        for dy in (-1, 0, 1):
            yield x, py + dy

def consider_move(positions, pos, move_order):
    if all(p not in positions for p in surrounding_positions(pos)):
        # no surrounding elves, don't move
        return pos
    for move in move_order:
        if all(p not in positions for p in positions_in_direction(pos, move)):
            # try to move in this direction
            px, py = pos
            mx, my = move
            return px+mx, py+my
    # no valid moves found
    return pos    

def step(positions, move_order):
    considered_positions = dict()
    for pos in positions:
        considered_positions[pos] = consider_move(positions, pos, move_order)
    target_counts = Counter(considered_positions.values())
    new_positions = set()
    for pos, target in considered_positions.items():
        if target_counts[target] > 1:
            new_pos = pos
        else:
            new_pos = target
        assert new_pos not in new_positions
        new_positions.add(new_pos)
    return new_positions

INITIAL_MOVE_ORDER = [
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0),
]

def solve1(input):
    positions = parse(input)
    move_order = list(INITIAL_MOVE_ORDER)
    for _ in range(10):
        positions = step(positions, move_order)
        move_order.append(move_order[0])
        del move_order[0]
    #print_rectangle(positions)
    rectange_size = (
        (1 + max(x for x,_ in positions) - min(x for x,_ in positions)) *
        (1 + max(y for _,y in positions) - min(y for _,y in positions)))
    return rectange_size - len(positions)

def solve2(input):
    positions = parse(input)
    move_order = list(INITIAL_MOVE_ORDER)
    n = 0
    while True:
        n += 1
        new_positions = step(positions, move_order)
        if new_positions == positions:
            #print_rectangle(positions)
            return n
        positions = new_positions
        move_order.append(move_order[0])
        del move_order[0]

assert solve1(EXAMPLE) == 110
assert solve2(EXAMPLE) == 20

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
