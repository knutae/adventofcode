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

def bounding_area(cubes):
    low = min(x for x,_,_ in cubes) - 1, min(y for _,y,_ in cubes) - 1, min(z for _,_,z in cubes) - 1
    high = max(x for x,_,_ in cubes) + 2, max(y for _,y,_ in cubes) + 2, max(z for _,_,z in cubes) + 2
    return low, high

def detect_outside_area(cubes):
    low, high = bounding_area(cubes)
    xlow, ylow, zlow = low
    xhigh, yhigh, zhigh = high
    assert low not in cubes
    outside = {low}
    search_space = [low]
    while len(search_space) > 0:
        new_search_space = []
        for p in search_space:
            for np in adjacent(p):
                x, y, z = np
                if x >= xlow and y >= ylow and z >= zlow and x < xhigh and y < yhigh and z < zhigh and np not in outside and np not in cubes:
                    new_search_space.append(np)
                    outside.add(np)
        search_space = new_search_space
    return outside

def solve2(input):
    cubes = set(parse(input))
    outside = detect_outside_area(cubes)
    return sum(sum(1 for a in adjacent(p) if a in outside) for p in cubes)

assert solve1(EXAMPLE) == 64
assert solve2(EXAMPLE) == 58

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
