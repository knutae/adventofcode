EXAMPLE = '''
F10
N3
F7
R90
F11
'''

NORTH = (0,1)
SOUTH = (0,-1)
EAST = (1,0)
WEST = (-1,0)
DIRECTIONS = {'N': NORTH, 'S': SOUTH, 'E': EAST, 'W': WEST}
ROTATE_ORDER = [EAST, SOUTH, WEST, NORTH]

def parse(input):
    return [(line[0], int(line[1:])) for line in input.strip().split('\n')]

def rotate_right(index, degrees):
    assert degrees % 90 == 0
    return (index + degrees // 90) % 4

def rotate_left(index, degrees):
    assert degrees % 90 == 0
    #return rotate_right(index, 360 - degrees)
    return (index + 4 - degrees // 90) % 4

def move(position, direction, amount):
    return position[0] + direction[0] * amount, position[1] + direction[1] * amount

def solve1(instructions):
    direction_index = ROTATE_ORDER.index(EAST)
    position = (0,0)
    for action, value in instructions:
        if action == 'F':
            position = move(position, ROTATE_ORDER[direction_index], value)
        elif action == 'R':
            direction_index = rotate_right(direction_index, value)
        elif action == 'L':
            direction_index = rotate_left(direction_index, value)
        else:
            #print(action, value)
            assert action in DIRECTIONS
            position = move(position, DIRECTIONS[action], value)
    #print(position)
    return abs(position[0]) + abs(position[1])

def rotate_waypoint_left(waypoint, degrees):
    a = degrees // 90
    x, y = waypoint
    while a != 0:
        x, y = -y, x
        a -= 1
        assert a >= 0
    return x, y

def rotate_waypoint_right(waypoint, degrees):
    return rotate_waypoint_left(waypoint, 360 - degrees)

def solve2(instructions):
    position = (0,0)
    waypoint = (10, 1)
    for action, value in instructions:
        if action == 'F':
            position = move(position, waypoint, value)
        elif action == 'R':
            waypoint = rotate_waypoint_right(waypoint, value)
        elif action == 'L':
            waypoint = rotate_waypoint_left(waypoint, value)
        else:
            #print(action, value)
            assert action in DIRECTIONS
            waypoint = move(waypoint, DIRECTIONS[action], value)
        #print(action, value, "->", position, waypoint)
    #print(position)
    return abs(position[0]) + abs(position[1])

assert solve1(parse(EXAMPLE)) == 25
assert solve2(parse(EXAMPLE)) == 286

with open('input') as f:
    instructions = parse(f.read())
print(solve1(instructions))
print(solve2(instructions))
