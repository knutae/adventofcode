import collections
from functools import cache

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
    return frozenset(rocks), dimensions, start

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

def modulo(i, gi, size):
    if i < 0:
        dg = -1
    elif i >= size:
        dg = 1
    else:
        dg = 0
    return i % size, gi + dg

assert modulo(0, 0, 10) == (0, 0)
assert modulo(9, 0, 10) == (9, 0)
assert modulo(-1, 0, 10) == (9, -1)
assert modulo(10, 0, 10) == (0, 1)
assert modulo(0, -3, 11) == (0, -3)

def moves2(rocks, dimensions, pos):
    ogx, ogy, px, py = pos
    w, h = dimensions
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x, gx = modulo(px+dx, ogx, w)
        y, gy = modulo(py+dy, ogy, h)
        if (x,y) not in rocks:
            yield gx, gy, x, y

@cache
def full_grid_moves(rocks, dimensions, local_positions):
    relative_positions = set()
    for x,y in local_positions:
        relative_positions.update(moves2(rocks, dimensions, (0,0,x,y)))
    relative_positions_by_grid = collections.defaultdict(set)
    for gx, gy, x, y in relative_positions:
        relative_positions_by_grid[(gx,gy)].add((x,y))
    return {k: frozenset(v) for k, v in relative_positions_by_grid.items()}

@cache
def cached_union(positions1, positions2):
    return frozenset(positions1 | positions2)

def step2(rocks, dimensions, positions_by_grid):
    new_positions_by_grid = collections.defaultdict(frozenset)
    for grid_pos, local_positions in positions_by_grid.items():
        gx, gy = grid_pos
        for grid_pos_diff, new_local_positions in full_grid_moves(rocks, dimensions, local_positions).items():
            dgx, dgy = grid_pos_diff
            new_grid_pos = gx+dgx, gy+dgy
            new_positions_by_grid[new_grid_pos] = cached_union(new_positions_by_grid[new_grid_pos], new_local_positions)
    return new_positions_by_grid

def predict(history, n):
    assert len(history) >= 3
    derive = [b-a for a, b in zip(history, history[1:])]
    derive2 = [b-a for a, b in zip(derive, derive[1:])]
    last_derive2 = derive2[-1]
    assert all(x == last_derive2 for x in derive2[1:])
    last = history[-1]
    last_derive = derive[-1]
    return last + n*last_derive + (n+1) * n // 2 * last_derive2

assert predict([894, 1528, 2324, 3282], 1) == 4402
assert predict([894, 1528, 2324, 3282], 2) == 5684
assert predict([894, 1528, 2324, 3282], 3) == 7128

def solve2(data, steps, verbose=False):
    rocks, dimensions, start = parse(data)
    positions_by_grid = {(0,0): frozenset({start})}
    distinct_history = collections.defaultdict(list)
    for iteration in range(steps):
        positions_by_grid = step2(rocks, dimensions, positions_by_grid)
        distinct_counts = collections.Counter(positions_by_grid.values())
        distinct_set = frozenset(distinct_counts.keys())
        history = distinct_history[distinct_set]
        total_count = sum(len(p)*c for p,c in distinct_counts.items())
        history.append((iteration, total_count))
        if len(history) >= 3:
            cycle_length = history[-1][0] - history[-2][0]
            remaining = steps - iteration - 1
            if remaining % cycle_length == 0:
                return predict([x[1] for x in history], remaining // cycle_length)
        if verbose:
            cycle_length = 'unknown' if len(history) < 2 else history[-1][0] - history[-2][0]
            print(iteration, 'distinct history', history, 'cycle', cycle_length, 'total', total_count)
    return sum(len(p) for p in positions_by_grid.values())

assert solve2(EXAMPLE, 6) == 16
assert solve2(EXAMPLE, 10) == 50
assert solve2(EXAMPLE, 50) == 1594
assert solve2(EXAMPLE, 100) == 6536
assert solve2(EXAMPLE, 500) == 167004
assert solve2(EXAMPLE, 1000) == 668697
assert solve2(EXAMPLE, 5000) == 16733044

with open('input') as f:
    data = f.read()

print(solve1(data, 64))
print(solve2(data, 26501365))
