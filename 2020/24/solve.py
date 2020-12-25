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

def solve1(input):
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
    return len(black_tiles)

assert solve1(EXAMPLE) == 10

with open('input') as f:
    input = f.read()

print(solve1(input))
