
EXAMPLE = 'target area: x=20..30, y=-10..-5'
PUZZLE_INPUT = 'target area: x=117..164, y=-140..-89'

def parse_range(s):
    assert s[1] == '='
    parts = s[2:].split('..')
    return tuple(int(x) for x in parts)

def parse(data):
    parts = data.strip()[len('target area: '):].split(', ')
    return tuple(parse_range(x) for x in parts)

def apply_drag(vx):
    if vx >= 1:
        return vx - 1
    if vx <= -1:
        return vx + 1
    assert vx == 0
    return vx

def step(position, velocity):
    px, py = position
    vx, vy = velocity
    new_position = px + vx, py + vy
    new_velocity = apply_drag(vx), vy - 1
    return new_position, new_velocity

def hits_target_yrange(velocity, yrange):
    min_y, max_y = yrange
    position = (0,0)
    highest_y = 0
    while position[1] > max_y:
        position, velocity = step(position, velocity)
        highest_y = max(highest_y, position[1])
    return position[1] >= min_y, highest_y

def hits_target_range(velocity, xrange, yrange):
    min_x, max_x = xrange
    min_y, max_y = yrange
    position = (0,0)
    while True:
        position, velocity = step(position, velocity)
        x, y = position
        if y < min_y:
            return False
        if x >= min_x and x <= max_x and y >= min_y and y <= max_y:
            return True


def solve1(data):
    xrange, yrange = parse(data)
    result = 0
    # how to detect the max y velocity?
    for vy in range(200):
        hits, highest_y = hits_target_yrange((0, vy), yrange)
        if hits:
            #print(vy, highest_y)
            result = highest_y
    return result

def solve2(data):
    xrange, yrange = parse(data)
    result = list()
    # how to detect the max y velocity?
    for vy in range(min(yrange), 200):
        if not hits_target_yrange((0, vy), yrange)[0]:
            continue
        for vx in range(min(1, *xrange), max(0, *xrange)+1):
            if hits_target_range((vx, vy), xrange, yrange):
                result.append((vx, vy))
    #print(len(result), result)
    return len(result)

assert solve1(EXAMPLE) == 45
print(solve1(PUZZLE_INPUT))
assert solve2(EXAMPLE) == 112
print(solve2(PUZZLE_INPUT))
