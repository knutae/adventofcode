import itertools
import sys

class Moon:
    def __init__(self, pos, vel=None):
        self.pos = list(pos)
        self.vel = [0,0,0] if vel is None else list(vel)

    def __repr__(self):
        return f"Moon(pos={self.pos}, vel={self.vel})"

def parse_vector(s: str):
    assert s[0] == '<'
    assert s[-1] == '>'
    parts = s[1:-1].split(', ')
    assert len(parts) == 3
    return tuple(int(x.split('=', 1)[1]) for x in parts)

def parse(s):
    return [Moon(parse_vector(line.strip())) for line in s.strip().split('\n')]

def step(moons):
    # apply gravity
    for a, b in itertools.combinations(moons, 2):
        for i in range(3):
            if a.pos[i] < b.pos[i]:
                a.vel[i] += 1
                b.vel[i] -= 1
            elif a.pos[i] > b.pos[i]:
                a.vel[i] -= 1
                b.vel[i] += 1
            else:
                assert a.pos[i] == b.pos[i]
    # apply velocity
    for a in moons:
        for i in range(3):
            a.pos[i] += a.vel[i]

def total_energy(moons):
    return sum(sum(abs(x) for x in moon.pos) * sum(abs(x) for x in moon.vel) for moon in moons)

def test():
    example = '''
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>'''
    moons = parse(example)
    #print(moons)
    for _ in range(10):
        step(moons)
    assert total_energy(moons) == 179
    second_example = '''
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>'''
    moons = parse(second_example)
    for _ in range(100):
        step(moons)
    assert total_energy(moons) == 1940

test()

moons = parse(sys.stdin.read())
for _ in range(1000):
    step(moons)
print(total_energy(moons))
