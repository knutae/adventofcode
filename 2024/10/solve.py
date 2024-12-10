EXAMPLE = '''
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
'''

def parse(data):
    lines = data.strip().split('\n')
    heights = dict()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            heights[(x,y)] = int(c)
    size = len(lines[x]), len(lines)
    return size, heights

def adjacent(x, y):
    return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

def trailhead_score(heights, pos):
    assert heights[pos] == 0
    positions = {pos}
    for i in range(1, 10):
        new_positions = set()
        for x, y in positions:
            for new_pos in adjacent(x, y):
                if heights.get(new_pos) == i:
                    new_positions.add(new_pos)
        positions = new_positions
    return len(positions)

def solve1(data):
    size, heights = parse(data)
    w, h = size
    score = 0
    for y in range(h):
        for x in range(w):
            if heights[(x,y)] == 0:
                score += trailhead_score(heights, (x,y))
    return score

assert solve1(EXAMPLE) == 36

with open('input') as f:
    data = f.read()

print(solve1(data))
