import itertools
import sys

class Moon:
    def __init__(self, pos, vel=None):
        self.pos = list(pos)
        self.vel = [0,0,0] if vel is None else list(vel)

    def __repr__(self):
        return f"Moon(pos={self.pos}, vel={self.vel})"

    def key(self):
        return (tuple(self.pos), tuple(self.vel))

    def axis(self, i):
        return MoonAxis(self.pos[i], self.vel[i])

class MoonAxis:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def key(self):
        return (self.pos, self.vel)

def parse_vector(s: str):
    assert s[0] == '<'
    assert s[-1] == '>'
    parts = s[1:-1].split(', ')
    assert len(parts) == 3
    return tuple(int(x.split('=', 1)[1]) for x in parts)

def parse(s):
    return [Moon(parse_vector(line.strip())) for line in s.strip().split('\n')]

def step_i(moons, i):
    # apply gravity
    for a, b in itertools.combinations(moons, 2):
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
        a.pos[i] += a.vel[i]

def step(moons):
    for i in range(3):
        step_i(moons, i)

def step_axis(moon_axes):
    for a, b in itertools.combinations(moon_axes, 2):
        if a.pos < b.pos:
            a.vel += 1
            b.vel -= 1
        elif a.pos > b.pos:
            a.vel -= 1
            b.vel += 1
        else:
            assert a.pos == b.pos
    for a in moon_axes:
        a.pos += a.vel

def total_energy(moons):
    return sum(sum(abs(x) for x in moon.pos) * sum(abs(x) for x in moon.vel) for moon in moons)

def moons_key(moons):
    return tuple(moon.key() for moon in moons)

def steps_until_cycle(moons):
    seen = set()
    while True:
        key = moons_key(moons)
        if key in seen:
            return len(seen)
        seen.add(key)
        step(moons)

def steps_until_cycle_axis(moon_axes):
    seen = set()
    while True:
        key = tuple(a.key() for a in moon_axes)
        if key in seen:
            return len(seen)
        seen.add(key)
        step_axis(moon_axes)

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def lcm_list(v):
    r = v[0]
    for a in v[1:]:
        r = lcm(r, a)
    return r

def fast_steps_until_cycle(moons):
    cycles = []
    for i in range(3):
        moon_axes = [moon.axis(i) for moon in moons]
        cycles.append(steps_until_cycle_axis(moon_axes))
    #print(cycles)
    return lcm_list(cycles)

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

    steps1 = steps_until_cycle(parse(example))
    #print(steps1)
    assert steps1 == 2772
    assert fast_steps_until_cycle(parse(example)) == 2772
    steps2 = fast_steps_until_cycle(parse(second_example))
    #print(steps2)
    assert steps2 == 4686774924

test()

def main():
    moons = parse(sys.stdin.read())
    #for _ in range(1000):
    #    step(moons)
    #print(total_energy(moons))
    print(fast_steps_until_cycle(moons))

main()
