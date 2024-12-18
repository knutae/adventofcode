EXAMPLE = '''
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
'''

def parse(data):
    return [tuple(int(x) for x in line.split(',')) for line in data.strip().split('\n')]

def adjacent(p, size):
    x, y = p
    if x > 0:
        yield (x-1, y)
    if x < size-1:
        yield (x+1, y)
    if y > 0:
        yield (x, y-1)
    if y < size-1:
        yield (x, y+1)

def solve1(data, size=71, limit=1024):
    points = parse(data)
    corrupted = set(points[:limit])
    visited = {(0,0)}
    target = (size-1,size-1)
    steps = 0
    current = {(0,0)}
    while target not in visited:
        steps += 1
        next_points = []
        for p in current:
            for q in adjacent(p, size):
                if q in visited or q in corrupted:
                    continue
                next_points.append(q)
                visited.add(q)
        current = next_points
    return steps

assert solve1(EXAMPLE, 7, 12) == 22

with open('input') as f:
    data = f.read()

print(solve1(data))
