import math
from itertools import combinations

EXAMPLE = '''
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
'''

def parse(s):
    lines = s.strip().split('\n')
    return [tuple(int(x) for x in line.split(',')) for line in lines]

def square_distance(a, b):
    ax, ay, az = a
    bx, by, bz = b
    return (ax - bx)**2 + (ay - by)**2 + (az - bz)**2

def solve1(s, connections):
    junctions = parse(s)
    pairs = list(combinations(junctions, 2))
    pairs.sort(key=lambda x:square_distance(*x))
    circuits = {x: {x} for x in junctions}
    for a, b in pairs[:connections]:
        circuits[a].update(circuits[b])
        for x in circuits[a]:
            if x != a:
                circuits[x] = circuits[a]
    unique_cirtcuits = set(frozenset(a) for a in circuits.values())
    sizes = [len(x) for x in unique_cirtcuits]
    sizes.sort(reverse=True)
    #print(sizes)
    return math.prod(sizes[:3])

assert solve1(EXAMPLE, 10) == 40

def solve2(s):
    junctions = parse(s)
    pairs = list(combinations(junctions, 2))
    pairs.sort(key=lambda x:square_distance(*x))
    circuits = {x: {x} for x in junctions}
    for a, b in pairs:
        circuits[a].update(circuits[b])
        if len(circuits[a]) == len(junctions):
            return a[0] * b[0]
        for x in circuits[a]:
            if x != a:
                circuits[x] = circuits[a]
    assert False

assert solve2(EXAMPLE) == 25272

with open('input') as f:
    s = f.read()

print(solve1(s, 1000))
print(solve2(s))
