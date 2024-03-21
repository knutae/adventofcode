import itertools

EXAMPLE = '''
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
'''

def parse_vec(vec):
    return [int(x.strip()) for x in vec.split(',')]

def parse_line(line):
    pos, vel = line.split('@')
    return parse_vec(pos), parse_vec(vel)

def parse(data):
    return [parse_line(line) for line in data.strip().split('\n')]

# x = Px - Vx*t, y = Py - Vy*t
# Vx*t = Px - x, y = Py - Vy*t
# t = (Px - x) / Vx, y = Py - Vy*t
# y = Py - Vy * ((Px - x) / Vx)
# y = Py - (Px - x) * Vy / Vx
# y = (Py - Px * Vy / Vx) + (Vy / Vx) * x

# (Py1 - Px1 * Vy1 / Vx1) + (Vy1 / Vx1) * x = (Py2 - Px2 * Vy2 / Vx2) + (Vy2 / Vx2) * x
# (Vy1 / Vx1) * x - (Vy2 / Vx2) * x = (Py2 - Px2 * Vy2 / Vx2) - (Py1 - Px1 * Vy1 / Vx1)
# (Vy1 / Vx1 - Vy2 / Vx2) * x = (Py2 - Px2 * Vy2 / Vx2) - (Py1 - Px1 * Vy1 / Vx1)
# x = ((Py2 - Px2 * Vy2 / Vx2) - (Py1 - Px1 * Vy1 / Vx1)) / (Vy1 / Vx1 - Vy2 / Vx2)
# x = (Py2 - Py1 - Px2 * Vy2 / Vx2 + Px1 * Vy1 / Vx1) / (Vy1 / Vx1 - Vy2 / Vx2)

# t = (Px - x) / Vx

def unpack_2d(line):
    pos, vel = line
    px, py, _ = pos
    vx, vy, _ = vel
    return px, py, vx, vy

def calculate_x(line1, line2):
    px1, py1, vx1, vy1 = unpack_2d(line1)
    px2, py2, vx2, vy2 = unpack_2d(line2)
    dv1 = vy1 / vx1
    dv2 = vy2 / vx2
    assert dv1 != dv2 # fixme
    return (py2 - py1 - px2 * dv2 + px1 * dv1) / (dv1 - dv2)

def calculate_time(line, x):
    pos, vel = line
    px = pos[0]
    vx = vel[0]
    return (px - x) / vx

def solve1(data, ):
    lines = parse(data)
    for line1, line2 in itertools.combinations(lines, 2):
        pass