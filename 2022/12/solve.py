EXAMPLE = '''
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''

def parse(input):
    heights = dict()
    start = None
    end = None
    for y, line in enumerate(input.strip().split('\n')):
        for x, c in enumerate(line):
            if c == 'S':
                start = (x, y)
                height = 0
            elif c == 'E':
                end = (x, y)
                height = 25
            else:
                height = ord(c) - ord('a')
            heights[(x, y)] = height
    return heights, start, end

def directions(x, y):
    yield x, y-1
    yield x-1, y
    yield x+1, y
    yield x, y+1

def solve1(input):
    heights, start, end = parse(input)
    distances = {start: 0}
    coords = {start}
    while end not in distances:
        new_coords = set()
        for x, y in coords:
            height = heights[(x, y)]
            distance = distances[(x, y)]
            for nx, ny in directions(x, y):
                if (nx, ny) not in heights or heights[(nx, ny)] > height + 1:
                    # no path
                    continue
                if (nx, ny) in distances:
                    # already visited
                    assert distances[(nx, ny)] <= distance + 1
                    continue
                distances[(nx, ny)] = distance + 1
                new_coords.add((nx, ny))
        coords = new_coords
    return distances[end]

def solve2(input):
    heights, _, end = parse(input)
    distances = {c: 0 for c in heights.keys() if heights[c] == 0}
    coords = set(distances.keys())
    while end not in distances:
        new_coords = set()
        for x, y in coords:
            height = heights[(x, y)]
            distance = distances[(x, y)]
            for nx, ny in directions(x, y):
                if (nx, ny) not in heights or heights[(nx, ny)] > height + 1:
                    # no path
                    continue
                if (nx, ny) in distances:
                    # already visited
                    assert distances[(nx, ny)] <= distance + 1
                    continue
                distances[(nx, ny)] = distance + 1
                new_coords.add((nx, ny))
        coords = new_coords
    return distances[end]

assert solve1(EXAMPLE) == 31
assert solve2(EXAMPLE) == 29

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
