import sys
import string
import typing

class Position(typing.NamedTuple):
    x: int
    y: int

class SearchKey(typing.NamedTuple):
    pos: Position
    keys: typing.FrozenSet[str]

class Dungeon(typing.NamedTuple):
    grid: typing.List[typing.List[str]]
    width: int
    height: int
    start_pos: Position
    all_keys: typing.FrozenSet[str]

KEY_RANGE = range(ord('a'), ord('z')+1)
DOOR_RANGE = range(ord('A'), ord('Z')+1)

def is_key(c):
    return ord(c) in KEY_RANGE

def is_door(c):
    return ord(c) in DOOR_RANGE

def parse(s):
    grid = s.strip().split('\n')
    width = len(grid[0])
    height = len(grid)
    all_keys = set()
    start_pos = None
    for y, line in enumerate(grid):
        assert len(line) == width
        for x, c in enumerate(line):
            if c == '@':
                assert start_pos is None
                start_pos = Position(x, y)
            elif is_key(c):
                assert c not in all_keys
                all_keys.add(c)
    assert start_pos is not None
    return Dungeon(
        grid=grid,
        width=width,
        height=height,
        start_pos=start_pos,
        all_keys=frozenset(all_keys),
    )

def try_move_to(grid, keys, pos):
    c = grid[pos.y][pos.x]
    if c == '#':
        return None
    if c == '.' or c == '@':
        return SearchKey(pos, keys)
    if is_key(c):
        return SearchKey(pos, keys | {c})
    if is_door(c):
        if c.lower() in keys:
            return SearchKey(pos, keys)
        else:
            return None
    assert False    

def enumerate_moves(grid, key):
    x, y = key.pos
    for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        new_key = try_move_to(grid, key.keys, Position(nx, ny))
        if new_key is not None:
            yield new_key

def solve(dungeon: Dungeon):
    start = SearchKey(dungeon.start_pos, frozenset())
    target_keys = dungeon.all_keys
    grid = dungeon.grid
    visited = {start}
    current_keys = {start}
    steps = 0
    while True:
        steps += 1
        new_keys = set()
        for key in current_keys:
            for move in enumerate_moves(grid, key):
                if move not in visited:
                    new_keys.add(move)
                    if move.keys == target_keys:
                        print(f"Solved: {move}, {steps} steps")
                        return steps
        current_keys = new_keys
        visited |= new_keys

def test():
    assert solve(parse('''
#########
#b.A.@.a#
#########''')) == 8
    assert solve(parse('''
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################''')) == 86
    assert solve(parse('''
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################''')) == 132
    assert solve(parse('''
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################''')) == 136
    assert solve(parse('''
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################''')) == 81

test()

def main():
    with open('input') as f:
        dungeon = parse(f.read())
    solve(dungeon)

main()