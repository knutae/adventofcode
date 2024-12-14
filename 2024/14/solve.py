EXAMPLE='''
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
'''

def parse_vec2(s):
    a, b = s.split(',')
    return int(a), int(b)

def parse_line(line):
    p, v = line.split(' ')
    assert p.startswith('p=') and v.startswith('v=')
    return parse_vec2(p[2:]), parse_vec2(v[2:])

def parse(data):
    return [parse_line(line) for line in data.strip().split('\n')]

def step_robot(p, v, w, h):
    px, py = p
    vx, vy = v
    return ((px + vx) % w, (py + vy) % h), v

def step(robots, w, h):
    return [step_robot(p, v, w, h) for (p, v) in robots]

def solve1(data, w, h):
    robots = parse(data)
    for _ in range(100):
        robots = step(robots, w, h)
    up_left = up_right = down_left = down_right = 0
    for (p, _) in robots:
        x, y = p
        if x < w // 2:
            if y < h // 2:
                up_left += 1
            elif y > h // 2:
                down_left += 1
        elif x > w // 2:
            if y < h // 2:
                up_right += 1
            elif y > h // 2:
                down_right += 1
    return up_left * up_right * down_left * down_right

assert solve1(EXAMPLE, 11, 7) == 12

with open('input') as f:
    data = f.read()

print(solve1(data, 101, 103))
