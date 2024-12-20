EXAMPLE = '''
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
'''

def parse(data):
    lines = data.strip().split('\n')
    start = None
    end = None
    walls = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            pos = x,y
            if c == '#':
                walls.add(pos)
            elif c == 'S':
                start = pos
            elif c == 'E':
                end = pos
            else:
                assert c == '.'
    return walls, start, end

def adjacent(pos, dist):
    x,y = pos
    return [(x-dist,y), (x+dist,y), (x,y-dist), (x,y+dist)]

def cheats_at(path, pos):
    cheat_lengths = []
    s = path[pos]
    for q in adjacent(pos, 2):
        if q in path and path[q] > s + 2:
            cheat_lengths.append(path[q] - s - 2)
    return cheat_lengths

def solve1(data, min_save=100):
    walls, start, end = parse(data)
    path = {start: 0}
    path_list = [start]
    pos = start
    while pos != end:
        next = []
        for q in adjacent(pos, 1):
            if q not in path and q not in walls:
                next.append(q)
        assert len(next) == 1
        pos = next[0]
        path[pos] = len(path)
        path_list.append(pos)
    r = 0
    for pos in path_list:
        for cheat_length in cheats_at(path, pos):
            if cheat_length >= min_save:
                r += 1
    return r

assert solve1(EXAMPLE, 20) == 5

with open('input') as f:
    data = f.read()

print(solve1(data))
