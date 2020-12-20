import functools
import collections
import operator

EXAMPLE = '''
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
'''

def parse_tile(input):
    lines = input.split('\n')
    header = lines[0]
    assert header.startswith('Tile ') and header.endswith(':')
    tile_num = int(header[5:-1])
    tile_data = lines[1:]
    return tile_num, tile_data

def parse(input):
    return [parse_tile(tile) for tile in input.strip().split('\n\n')]

def edge_set(tile_data):
    edges = set()
    def add(s):
        edges.add(s)
        edges.add(''.join(reversed(s)))
    add(tile_data[0])
    add(tile_data[-1])
    add(''.join(t[0] for t in tile_data))
    add(''.join(t[-1] for t in tile_data))
    assert len(edges) == 8 # all unique and non-symmetric?
    return edges

def all_other_edges(tiles, tile_num):
    other_edges = set()
    for num in tiles:
        if num != tile_num:
            other_edges |= edge_set(tiles[num])
    return other_edges

def detect_corner_tiles(tiles):
    #edges = {num: edge_set(tiles[num]) for num in tiles}
    def count_unique_edges(tile_num):
        count = 0
        other_edges = all_other_edges(tiles, tile_num)
        for edge in edge_set(tiles[tile_num]):
            if edge not in other_edges:
                count += 1
        return count
    # corners have 4 unique edges, including flipped ones
    corner_tiles = [num for num in tiles if count_unique_edges(num) == 4]
    assert len(corner_tiles) == 4
    return corner_tiles

def rotate_tile(tile_data):
    assert len(tile_data) == len(tile_data[0])
    size = len(tile_data)
    new_tile = []
    for y in range(size):
        new_tile.append(''.join(tile_data[size-x-1][y] for x in range(size)))
    return new_tile

def flip_vertical(tile_data):
    return list(reversed(tile_data))

def upper_edge(tile_data):
    return tile_data[0]

def lower_edge(tile_data):
    return tile_data[-1]

def left_edge(tile_data):
    return ''.join(t[0] for t in tile_data)

def right_edge(tile_data):
    return ''.join(t[-1] for t in tile_data)

def upper_left_corner(tiles, tile_num):
    tile_data = tiles[tile_num]
    other_edges = all_other_edges(tiles, tile_num)
    rotations = 0
    while upper_edge(tile_data) in other_edges or left_edge(tile_data) in other_edges:
        tile_data = rotate_tile(tile_data)
        rotations += 1
        assert rotations < 4
    yield tile_data
    # to get the other valid arrangement, flip vertical and rotate once
    tile_data = flip_vertical(tile_data)
    tile_data = rotate_tile(tile_data)
    assert upper_edge(tile_data) not in other_edges and left_edge(tile_data) not in other_edges
    yield tile_data

def generate_tile_arrangements(tile_data):
    for i in range(4):
        yield tile_data
        tile_data = rotate_tile(tile_data)
    tile_data = flip_vertical(tile_data)
    for i in range(4):
        yield tile_data
        tile_data = rotate_tile(tile_data)

def find_tile_arrangement(tile_data, predicate):
    for tile_data in generate_tile_arrangements(tile_data):
        if predicate(tile_data):
            return tile_data
    assert False

def build_edge_map(tiles):
    edge_map = collections.defaultdict(set)
    for tile_num, tile_data in tiles.items():
        for edge in edge_set(tile_data):
            edge_map[edge].add(tile_num)
    return edge_map

def arrange_row(tiles, edge_map, first_tile_num, first_tile_data):
    tiles_row = [(first_tile_num, first_tile_data)]
    while True:
        last_tile_num, last_tile_data = tiles_row[-1]
        edge = right_edge(last_tile_data)
        candidates = edge_map[edge]
        assert len(candidates) == 1 or len(candidates) == 2
        if len(candidates) == 1:
            assert next(iter(candidates)) == last_tile_num
            break
        next_tile_num = [c for c in candidates if c != last_tile_num][0]
        next_tile_data = find_tile_arrangement(tiles[next_tile_num], lambda t: left_edge(t) == edge)
        tiles_row.append((next_tile_num, next_tile_data))
    return tiles_row

def arrange_column(tiles, edge_map, first_tile_num, first_tile_data):
    tiles_col = [(first_tile_num, first_tile_data)]
    while True:
        last_tile_num, last_tile_data = tiles_col[-1]
        edge = lower_edge(last_tile_data)
        candidates = edge_map[edge]
        assert len(candidates) == 1 or len(candidates) == 2
        if len(candidates) == 1:
            assert next(iter(candidates)) == last_tile_num
            break
        next_tile_num = [c for c in candidates if c != last_tile_num][0]
        next_tile_data = find_tile_arrangement(tiles[next_tile_num], lambda t: upper_edge(t) == edge)
        tiles_col.append((next_tile_num, next_tile_data))
    return tiles_col

def arrange_grid(tiles, edge_map, first_tile_num, first_tile_data):
    return [
        arrange_row(tiles, edge_map, tile_num, tile_data)
        for tile_num, tile_data in arrange_column(tiles, edge_map, first_tile_num, first_tile_data)
    ]

def join_grid(grid):
    tile_size = len(grid[0][0][1])
    rows = []
    for tile_row in grid:
        for y in range(1, tile_size-1):
            current_row = []
            for tile_num, tile_data in tile_row:
                current_row.append(tile_data[y][1:-1])
            rows.append(''.join(current_row))
    return rows

SEA_MONSTER = [
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   ',
]

SEA_MONSTER_PIXELS = {
    (x,y)
    for y, row in enumerate(SEA_MONSTER)
    for x, c in enumerate(row)
    if c == '#'
}

def has_sea_monster_at(grid, px, py):
    assert py >= 0 and py < len(grid) - len(SEA_MONSTER)
    assert px >= 0 and px < len(grid[0]) - len(SEA_MONSTER[0])
    return all(grid[sy+py][sx+px] == '#' for sx,sy in SEA_MONSTER_PIXELS)

def count_sea_monsters(grid):
    count = 0
    for y in range(len(grid) - len(SEA_MONSTER)):
        for x in range(len(grid[0]) - len(SEA_MONSTER[0])):
            if has_sea_monster_at(grid, x, y):
                count += 1
    return count

#tiles = parse(EXAMPLE)
#tile_data = tiles[0][1]
#print('\n'.join(tile_data))
#print('------------')
#print('\n'.join(rotate_tile(tile_data)))

def solve1(input):
    tiles = dict(parse(input))
    corner_tiles = detect_corner_tiles(tiles)
    return functools.reduce(operator.mul, corner_tiles, 1)

def solve2(input):
    tiles = dict(parse(input))
    edge_map = build_edge_map(tiles)
    corner_tiles = detect_corner_tiles(tiles)
    for tile_num in corner_tiles:
        for tile_data in upper_left_corner(tiles, tile_num):
            grid = join_grid(arrange_grid(tiles, edge_map, tile_num, tile_data))
            sea_monsters = count_sea_monsters(grid)
            if sea_monsters > 0:
                #print('\n'.join(grid))
                #print(f'Number of sea monsters: {count_sea_monsters(grid)}')
                # safe to assume no overlapping sea monsters?
                total_hashes = ''.join(grid).count('#')
                result = total_hashes - len(SEA_MONSTER_PIXELS) * sea_monsters
                return result


assert solve1(EXAMPLE) == 20899048083289
assert solve2(EXAMPLE) == 273

with open('input') as f:
    input = f.read()
print(solve1(input))
print(solve2(input))
