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

def create_new_shape_pos(tower, shape):
    tower_height = 0 if len(tower) == 0 else 1 + max(y for _, y in tower)
    return 2, 3 + tower_height

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
    for shape_index in range(2022):
        shape = SHAPES[shape_index % len(SHAPES)]
        shape_pos = create_new_shape_pos(tower, shape)
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
    return 1 + max(y for _, y in tower)

assert solve1(EXAMPLE) == 3068

with open('input') as f:
    input = f.read()

print(solve1(input))
