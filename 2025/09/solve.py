from itertools import combinations

EXAMPLE = '''
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
'''

def parse(s):
    lines = s.strip().split('\n')
    return [tuple(int(x) for x in line.split(',')) for line in lines]

def area(a, b):
    ax, ay = a
    bx, by = b
    return (abs(ax-bx)+1) * (abs(ay-by)+1)

def solve1(s):
    coords = parse(s)
    return max(area(a, b) for a, b in combinations(coords, 2))

assert solve1(EXAMPLE) == 50

with open('input') as f:
    s = f.read()

print(solve1(s))
