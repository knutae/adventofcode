import functools
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

def detect_corner_tiles(tiles):
    edges = {num: edge_set(tiles[num]) for num in tiles}
    def count_unique_edges(tile_num):
        count = 0
        other_edges = set()
        for num in tiles:
            if num != tile_num:
                other_edges |= edges[num]
        for edge in edges[tile_num]:
            if edge not in other_edges:
                count += 1
        return count
    # corners have 4 unique edges, including flipped ones
    corner_tiles = [num for num in tiles if count_unique_edges(num) == 4]
    assert len(corner_tiles) == 4
    return corner_tiles

def solve1(input):
    tiles = dict(parse(input))
    corner_tiles = detect_corner_tiles(tiles)
    return functools.reduce(operator.mul, corner_tiles, 1)

assert solve1(EXAMPLE) == 20899048083289

with open('input') as f:
    input = f.read()
print(solve1(input))
