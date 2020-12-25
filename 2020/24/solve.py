EXAMPLE = '''
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
'''

def hex_move(x, y, direction):
    if direction == 'e':
        return x+1, y
    if direction == 'w':
        return x-1, y
    even = y % 2
    odd = 1 - even
    if direction == 'ne':
        return x+even, y-1
    if direction == 'nw':
        return x-odd, y-1
    if direction == 'se':
        return x+even, y+1
    if direction == 'sw':
        return x-odd, y+1
    assert False

assert hex_move(3, 2, 'e') == (4, 2)
assert hex_move(3, 2, 'w') == (2, 2)
assert hex_move(3, 2, 'ne') == (3, 1)
assert hex_move(3, 2, 'nw') == (2, 1)
assert hex_move(3, 2, 'se') == (3, 3)
assert hex_move(3, 2, 'sw') == (2, 3)
assert hex_move(3, 3, 'e') == (4, 3)
assert hex_move(3, 3, 'w') == (2, 3)
assert hex_move(3, 3, 'ne') == (4, 2)
assert hex_move(3, 3, 'nw') == (3, 2)
assert hex_move(3, 3, 'se') == (4, 4)
assert hex_move(3, 3, 'sw') == (3, 4)

def parse_directions(line):
    result = []
    i = 0
    while i < len(line):
        if line[i] in 'ns':
            assert line[i+1] in 'ew'
            result.append(line[i:i+2])
            i += 2
        else:
            assert line[i] in 'ew'
            result.append(line[i])
            i += 1
    return result

def parse(input):
    return [parse_directions(line) for line in input.strip().split('\n')]

def initial_black_tiles(input):
    black_tiles = set()
    for directions in parse(input):
        x, y = 0, 0
        for d in directions:
            x, y = hex_move(x, y, d)
        tile = x, y
        if tile in black_tiles:
            black_tiles.remove(tile)
        else:
            black_tiles.add(tile)
    return black_tiles

def solve1(input):
    return len(initial_black_tiles(input))

assert solve1(EXAMPLE) == 10

def generate_adjacent_tiles(x, y):
    yield x+1, y
    yield x-1, y
    even = y % 2
    odd = 1 - even
    yield x+even, y-1
    yield x-odd, y-1
    yield x+even, y+1
    yield x-odd, y+1

def count_adjacent_black_tiles(x, y, black_tiles):
    count = 0
    for ax, ay in generate_adjacent_tiles(x, y):
        if (ax, ay) in black_tiles:
            count += 1
        if count == 3:
            # never need to count to more than 3 for correctness
            break
    return count

def step(black_tiles):
    min_x = min(pos[0] for pos in black_tiles)
    max_x = max(pos[0] for pos in black_tiles)
    min_y = min(pos[1] for pos in black_tiles)
    max_y = max(pos[1] for pos in black_tiles)
    next_black_tiles = set()
    for x in range(min_x-1, max_x+2):
        for y in range(min_y-1, max_y+2):
            if (x,y) in black_tiles:
                # black: flip to white with zero or more than 2 adjacent black tiles
                count = count_adjacent_black_tiles(x, y, black_tiles)
                if count == 0 or count > 2:
                    pass # flip to white: no-op
                else:
                    next_black_tiles.add((x,y)) # don't flip
            else:
                # white: flip to black with exactly 2 adjacent black tiles
                count = count_adjacent_black_tiles(x, y, black_tiles)
                if count == 2:
                    next_black_tiles.add((x,y)) # flip to black
    return next_black_tiles

def solve2(input):
    black_tiles = initial_black_tiles(input)
    for i in range(100):
        black_tiles = step(black_tiles)
        #print(f'Day {i+1}: {len(black_tiles)}')
    return len(black_tiles)

assert solve2(EXAMPLE) == 2208

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
