EXAMPLE = '''
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
'''

def parse_brick(line):
    return tuple(tuple(int(v) for v in part.split(',')) for part in line.split('~'))

def lower_brick_z(brick):
    a,b = brick
    return min(a[2], b[2])

def upper_brick_z(brick):
    a,b = brick
    return max(a[2], b[2])

def parse(data):
    bricks = [parse_brick(line) for line in data.strip().split('\n')]
    bricks.sort(key=lower_brick_z)
    return bricks

def brick_coordinates(brick):
    p,q = brick
    x1,y1,z1 = p
    x2,y2,z2 = q
    for x in range(min(x1,x2), max(x1,x2)+1):
        for y in range(min(y1,y2), max(y1,y2)+1):
            for z in range(min(z1,z2), max(z1,z2)+1):
                yield x,y,z

def move_to_height(brick, z):
    p,q = brick
    x1,y1,z1 = p
    x2,y2,z2 = q
    dz = min(z1, z2)-z
    return ((x1,y1,z1-dz), (x2,y2,z2-dz))

assert move_to_height(((5,5,10),(5,5,30)), 1) == ((5,5,1), (5,5,21))

def drop_brick(tower, brick):
    if len(tower) == 0:
        return move_to_height(brick, 1)
    current_z = lower_brick_z(brick)
    height = max(z for _,_,z in tower)
    for z in range(min(height, current_z-1),0,-1):
        if any(p in tower for p in brick_coordinates(move_to_height(brick, z))):
            return move_to_height(brick, z+1)
    return move_to_height(brick, 1)

def can_disintegrate(bricks, brick, tower):
    shaky_tower = tower - set(brick_coordinates(brick))
    assert shaky_tower != tower
    upper_z = upper_brick_z(brick)
    for other_brick in bricks:
        if lower_brick_z(other_brick) != upper_z + 1:
            # only check bricks that could be touching the removed brick in the z direction
            continue
        shakier_tower = shaky_tower - set(brick_coordinates(other_brick))
        if drop_brick(shakier_tower, other_brick) != other_brick:
            return False
    return True

def solve1(data):
    bricks = parse(data)
    tower = set()
    for i, brick in enumerate(bricks):
        brick = drop_brick(tower, brick)
        bricks[i] = brick
        tower.update(brick_coordinates(brick))
    return sum(1 for brick in bricks if can_disintegrate(bricks, brick, tower))

assert solve1(EXAMPLE) == 5

with open('input') as f:
    data = f.read()

print(solve1(data))
