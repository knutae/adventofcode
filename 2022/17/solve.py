EXAMPLE = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'

SHAPES = [
    # ####
    frozenset({(0,0), (1,0), (2,0), (3,0)}),
    # .#.
    # ###
    # .#.
    frozenset({(1,0), (0,1), (1,1), (2,1), (1,2)}),
    # ..#
    # ..#
    # ###
    frozenset({(0,0), (1,0), (2,0), (2,1), (2,2)}),
    # #
    # #
    # #
    # #
    frozenset({(0,0), (0,1), (0,2), (0,3)}),
    # ##
    # ##
    frozenset({(0,0), (1,0), (0,1), (1,1)}),
]

def shape_at(shape, pos):
    px, py = pos
    return frozenset((x+px,y+py) for x,y in shape)

def would_collide(tower, shape, shape_pos):
    return any((x < 0) or (x >= 7) or (y < 0) or (x,y) in tower for x, y in shape_at(shape, shape_pos))

def move_shape(tower, shape, shape_pos, direction):
    dx, dy = direction
    sx, sy = shape_pos
    new_shape_pos = (sx+dx, sy+dy)
    if would_collide(tower, shape, new_shape_pos):
        # can't move
        return shape_pos
    else:
        return new_shape_pos

def tower_height(tower):
    return 0 if len(tower) == 0 else 1 + max(y for _, y in tower)

def create_new_shape_pos(tower):
    return 2, 3 + tower_height(tower)

def parse_wind_directions(input):
    dirs = {'<':(-1, 0), '>': (1, 0)}
    return [dirs[c] for c in input.strip()]

def print_tower(tower, shape, shape_pos):
    shape = shape_at(shape, shape_pos)
    height = max(y for _, y in shape)
    print()
    for y in range(height, -1, -1):
        print('|' + ''.join('#' if (x,y) in tower else '@' if (x,y) in shape else '.' for x in range(7)) + '|')
    print('+-------+')

def solve1(input, verbose=False):
    tower = set()
    wind_directions = parse_wind_directions(input)
    wind_index = 0
    for i in range(2022):
        shape_index = i % len(SHAPES)
        shape = SHAPES[shape_index]
        shape_pos = create_new_shape_pos(tower)
        if verbose:
            print_tower(tower, shape, shape_pos)
        while True:
            # wind
            shape_pos = move_shape(tower, shape, shape_pos, wind_directions[wind_index])
            wind_index = (wind_index + 1) % len(wind_directions)
            # gravity
            new_shape_pos = move_shape(tower, shape, shape_pos, (0, -1))
            if new_shape_pos == shape_pos:
                # stopped due to gravity
                tower.update(shape_at(shape, shape_pos))
                break
            shape_pos = new_shape_pos
    return tower_height(tower)

def solve_by_cycle(heights_per_index, cycle_length, height_diff):
    for i, height in heights_per_index.values():
        remaining_steps = 1000000000000 - i - 1
        if remaining_steps % cycle_length == 0:
            remaining_cycles = remaining_steps // cycle_length
            return height + remaining_cycles * height_diff
    assert False

def solve2(input, verbose=False):
    tower = set()
    wind_directions = parse_wind_directions(input)
    wind_index = 0
    heights_per_index = dict()
    height_diffs = dict()
    cycle_length = None
    cycle_confidence = 0
    i = 0
    while True:
        shape_index = i % len(SHAPES)
        shape = SHAPES[shape_index]
        shape_pos = create_new_shape_pos(tower)
        if verbose:
            print_tower(tower, shape, shape_pos)
        while True:
            # wind
            shape_pos = move_shape(tower, shape, shape_pos, wind_directions[wind_index])
            wind_index = (wind_index + 1) % len(wind_directions)
            # gravity
            new_shape_pos = move_shape(tower, shape, shape_pos, (0, -1))
            if new_shape_pos == shape_pos:
                # stopped due to gravity
                tower.update(shape_at(shape, shape_pos))
                break
            shape_pos = new_shape_pos
        current_height = tower_height(tower)
        index = shape_index, wind_index
        if index in heights_per_index:
            old_i, old_height = heights_per_index[index]
            height_diff = current_height - old_height
            possible_cycle = all(h == height_diff for h in height_diffs.values())
            height_diffs[index] = height_diff
            if possible_cycle:
                if i - old_i == cycle_length:
                    cycle_confidence += 1
                    if cycle_confidence == cycle_length:
                        # remove outdated indexes
                        heights_per_index = {k:v for k, v in heights_per_index.items() if v[0] >= i - cycle_length}
                        #print(f'Cycle! length {cycle_length} height_diff {height_diff} confidence {cycle_confidence}')
                        return solve_by_cycle(heights_per_index, cycle_length, height_diff)
                else:
                    cycle_length =  i - old_i
                    cycle_confidence = 1
            else:
                cycle_length = None
                cycle_confidence = 0
        heights_per_index[index] = i, tower_height(tower)
        i += 1

assert solve1(EXAMPLE) == 3068
assert solve2(EXAMPLE) == 1514285714288

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
