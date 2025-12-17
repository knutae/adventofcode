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

def neighboroughs(p):
    x, y = p
    return [
        (x, y-1),
        (x-1, y),
        (x+1, y),
        (x, y+1),
    ]

def fill_grid(coords):
    grid = set()
    y_min = min(p[1] for p in coords)
    fill_start = None
    for a, b in zip(coords, coords[1:] + [coords[0]]):
        ax, ay = a
        bx, by = b
        if ax == bx:
            for y in range(min(ay, by), max(ay, by)+1):
                grid.add((ax, y))
        elif ay == by:
            for x in range(min(ax, bx), max(ax, bx)+1):
                grid.add((x, ay))
            if ay == y_min and fill_start is None:
                # pick a coordinate guaranteed to be inside the grid as the start
                fill_start = min(ax, bx) + 1, ay + 1
        else:
            assert False
    #print(len(grid))
    new_coords = {fill_start}
    while len(new_coords) > 0:
        #print(f"... {len(new_coords)} {len(grid)}")
        grid |= new_coords
        next_coords = set()
        for p in new_coords:
            for q in neighboroughs(p):
                if q not in grid:
                    next_coords.add(q)
        new_coords = next_coords
    #print(len(grid))
    return grid


def is_area_within_grid(a, b, grid):
    ax, ay = a
    bx, by = b
    for x in range(min(ax, bx), max(ax, bx)+1):
        for y in range(min(ay, by), max(ay, by)+1):
            if (x, y) not in grid:
                return False
    return True

def compress_coords(coords):
    x_coords = list(sorted({x for x, _ in coords}))
    y_coords = list(sorted({y for _, y in coords}))
    # map all indexes to even numbers to allow fill algorithm to work consistently
    x_coords = {i*2: x for i, x in enumerate(x_coords)}
    y_coords = {i*2: y for i, y in enumerate(y_coords)}
    reverse_x_coords = {b: a for a, b in x_coords.items()}
    reverse_y_coords = {b: a for a, b in y_coords.items()}
    compressed = [(reverse_x_coords[x], reverse_y_coords[y]) for x, y in coords]
    return compressed, x_coords, y_coords

def uncompress(p, x_coords, y_coords):
    px, py = p
    return x_coords[px], y_coords[py]

def solve2(s):
    full_coords = parse(s)
    compressed_coords, x_coords, y_coords = compress_coords(full_coords)
    compressed_grid = fill_grid(compressed_coords)
    return max(
        area(uncompress(a, x_coords, y_coords), uncompress(b, x_coords, y_coords))
        for a, b in combinations(compressed_coords, 2)
        if is_area_within_grid(a, b, compressed_grid))


assert solve2(EXAMPLE) == 24

with open('input') as f:
    s = f.read()

print(solve1(s))
print(solve2(s))
