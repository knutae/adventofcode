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
    start_positions: typing.Sequence[Position]
    all_keys: typing.FrozenSet[str]

class MultiSearchKey(typing.NamedTuple):
    robots: typing.FrozenSet[typing.Tuple[Position, int]]
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
    start_positions = []
    for y, line in enumerate(grid):
        assert len(line) == width
        for x, c in enumerate(line):
            if c == '@':
                assert Position(x, y) not in start_positions
                start_positions.append(Position(x, y))
            elif is_key(c):
                assert c not in all_keys
                all_keys.add(c)
    assert len(start_positions) > 0
    return Dungeon(
        grid=grid,
        width=width,
        height=height,
        start_positions=start_positions,
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
    start = SearchKey(dungeon.start_positions[0], frozenset())
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
    robots = dict(key.robots)
    old_count = robots[old_pos]
    assert old_count > 0
    if old_count == 1:
        del robots[old_pos]
    else:
        robots[old_pos] = old_count - 1
    if new_pos in robots:
        robots[new_pos] += 1
    else:
        robots[new_pos] = 1
    return MultiSearchKey(frozenset(robots.items()), new_keys)

def enumerate_multi_moves(grid, key: MultiSearchKey):
    for robot_pos, robot_count in key.robots:
        assert robot_count > 0
        x, y = robot_pos
        for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            pos = Position(nx, ny)
            keys = try_move_to(grid, key.keys, pos)
            if keys is not None:
                yield move_robot(key, robot_pos, pos, keys)

def solve_multi(dungeon: Dungeon):
    assert len(dungeon.start_positions) > 1
    start_robots = frozenset((pos, 1) for pos in dungeon.start_positions)
    start = MultiSearchKey(start_robots, frozenset())
    target_keys = dungeon.all_keys
    grid = dungeon.grid
    visited = {start}
    current_keys = {start}
    steps = 0
    while True:
        steps += 1
        new_keys = set()
        for key in current_keys:
            for move in enumerate_multi_moves(grid, key):
                if move not in visited:
                    new_keys.add(move)
                    if move.keys == target_keys:
                        print(f"Solved: {move}, {steps} steps")
                        return steps
        current_keys = new_keys
        visited |= new_keys
        #print(f"Step {steps} new keys {len(current_keys)} visited {len(visited)}")

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
#main_multi()
