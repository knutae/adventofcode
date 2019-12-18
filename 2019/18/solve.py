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
    start_positions: typing.FrozenSet[Position]
    all_keys: typing.FrozenSet[str]

class MultiSearchKey(typing.NamedTuple):
    robots: typing.FrozenSet[Position]
    keys: typing.FrozenSet[str]

KEY_RANGE = range(ord('a'), ord('z')+1)
DOOR_RANGE = range(ord('A'), ord('Z')+1)

def is_key(c):
    return ord(c) in KEY_RANGE

def is_door(c):
    return ord(c) in DOOR_RANGE

def join_keys(keys, new_key):
    assert new_key not in keys
    return ''.join(sorted(keys + new_key))

def parse(s):
    grid = s.strip().split('\n')
    width = len(grid[0])
    height = len(grid)
    all_keys = set()
    start_positions = set()
    for y, line in enumerate(grid):
        assert len(line) == width
        for x, c in enumerate(line):
            if c == '@':
                assert Position(x, y) not in start_positions
                start_positions.add(Position(x, y))
            elif is_key(c):
                assert c not in all_keys
                all_keys.add(c)
    assert len(start_positions) > 0
    return Dungeon(
        grid=grid,
        width=width,
        height=height,
        start_positions=frozenset(start_positions),
        all_keys=frozenset(all_keys),
    )

def try_move_to(grid, keys, pos):
    c = grid[pos.y][pos.x]
    if c == '#':
        return None
    if c == '.' or c == '@':
        return keys
    if is_key(c):
        if c in keys:
            return keys
        else:
            return keys | {c}
    if is_door(c):
        if c.lower() in keys:
            return keys
        else:
            return None
    assert False    

def enumerate_moves(grid, key: SearchKey):
    x, y = key.pos
    for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        pos = Position(nx, ny)
        keys = try_move_to(grid, key.keys, pos)
        if keys is not None:
            yield SearchKey(pos, keys)

def solve(dungeon: Dungeon):
    assert len(dungeon.start_positions) == 1
    start = SearchKey(next(iter(dungeon.start_positions)), frozenset())
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

def move_robot(key: MultiSearchKey, old_pos: Position, new_pos: Position, new_keys: typing.FrozenSet[str]):
    robots = set(key.robots)
    assert old_pos in robots
    assert new_pos not in robots
    robots.remove(old_pos)
    robots.add(new_pos)
    return MultiSearchKey(frozenset(robots), new_keys)

def enumerate_multi_moves_from_pos(robot_pos, grid, key: MultiSearchKey):
    x, y = robot_pos
    for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        pos = Position(nx, ny)
        if pos in key.robots:
            continue
        keys = try_move_to(grid, key.keys, pos)
        if keys is not None:
            yield move_robot(key, robot_pos, pos, keys), pos

def enumerate_all_multi_moves(grid, key: MultiSearchKey):
    for pos in key.robots:
        for move in enumerate_multi_moves_from_pos(pos, grid, key):
            yield move

def solve_multi(dungeon: Dungeon):
    assert len(dungeon.start_positions) > 1
    start = MultiSearchKey(dungeon.start_positions, frozenset())
    target_keys = dungeon.all_keys
    grid = dungeon.grid
    visited = {start}
    current_keys = {start: None}
    steps = 0
    while True:
        steps += 1
        new_keys = dict()
        for key, pos_or_none in current_keys.items():
            if pos_or_none is None:
                generator = enumerate_all_multi_moves(grid, key)
            else:
                generator = enumerate_multi_moves_from_pos(pos_or_none, grid, key)
            for move, new_pos in generator:
                if move not in visited:
                    if move.keys == target_keys:
                        print(f"Solved: {move}, {steps} steps")
                        return steps
                    if move.keys == key.keys:
                        # keys did not change, only continue search with the same robot, identified by its position
                        new_keys[move] = new_pos
                    else:
                        # keys changes, continue search with all robots
                        new_keys[move] = None
        current_keys = new_keys
        visited |= new_keys.keys()
        print(f"Step {steps} new keys {len(current_keys)} visited {len(visited)}")

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

def test_multi():
    assert solve_multi(parse('''
#######
#a.#Cd#
##@#@##
#######
##@#@##
#cB#Ab#
#######''')) == 8
    assert solve_multi(parse('''
###############
#d.ABC.#.....a#
######@#@######
###############
######@#@######
#b.....#.....c#
###############''')) == 24
    assert solve_multi(parse('''
#############
#DcBa.#.GhKl#
#.###@#@#I###
#e#d#####j#k#
###C#@#@###J#
#fEbA.#.FgHi#
#############''')) == 32
    assert solve_multi(parse('''
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############''')) == 72

def main():
    with open('input') as f:
        dungeon = parse(f.read())
    solve(dungeon)

def main_multi():
    with open('input2') as f:
        dungeon = parse(f.read())
    solve_multi(dungeon)

test()
test_multi()
#main()
main_multi()
