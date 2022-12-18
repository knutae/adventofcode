EXAMPLE = '''
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
'''

def parse(input):
    return [tuple(map(int, line.split(','))) for line in input.strip().split('\n')]

def adjacent(p):
    x, y, z = p
    yield x-1, y, z
    yield x+1, y, z
    yield x, y-1, z
    yield x, y+1, z
    yield x, y, z-1
    yield x, y, z+1

def solve1(input):
    cubes = set(parse(input))
    return sum(6 - sum(1 for a in adjacent(p) if a in cubes) for p in cubes)

assert solve1(EXAMPLE) == 64

with open('input') as f:
    input = f.read()

print(solve1(input))
