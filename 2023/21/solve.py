EXAMPLE = '''
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
'''

def parse(data):
    lines = data.strip().split('\n')
    rocks = set()
    start = None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                rocks.add((x,y))
            elif c == 'S':
                assert start is None
                start = (x,y)
            else:
                assert c == '.'
    dimensions = len(lines[0]), len(lines)
    return rocks, dimensions, start

def moves(rocks, dimensions, pos):
    px, py = pos
    w, h = dimensions
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x, y = px+dx, py+dy
        if x >= 0 and x < w and y >= 0 and y < h and (x,y) not in rocks:
            yield x, y

def step(rocks, dimensions, positions):
    new_positions = set()
    for pos in positions:
        new_positions.update(moves(rocks, dimensions, pos))
    return new_positions

def solve1(data, steps):
    rocks, dimensions, start = parse(data)
    positions = {start}
    for _ in range(steps):
        positions = step(rocks, dimensions, positions)
    return len(positions)

assert solve1(EXAMPLE, 6) == 16

with open('input') as f:
    data = f.read()

print(solve1(data, 64))
