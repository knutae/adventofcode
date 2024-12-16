EXAMPLE = '''
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
'''

EXAMPLE2 = '''
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
'''

def parse(data):
    walls = set()
    start = None
    end = None
    for y, line in enumerate(data.strip().split('\n')):
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

def turn_left(direction):
    dx, dy = direction
    return dy, -dx

def turn_right(direction):
    dx, dy = direction
    return -dy, dx

def enumerate_moves(pos, direction, walls):
    x, y = pos
    dx, dy = direction
    forward = x+dx, y+dy
    if forward not in walls:
        yield forward, direction, 1
    yield pos, turn_left(direction), 1000
    yield pos, turn_right(direction), 1000

def solve1(data):
    walls, start, end = parse(data)
    start_key = start, (1, 0)
    all_distances = {start_key: 0}
    next_keys = {start_key}
    while next_keys:
        #print(len(next_keys), len(all_distances))
        new_keys = set()
        for pos, direction in next_keys:
            before_cost = all_distances[(pos, direction)]
            for new_pos, new_direction, cost in enumerate_moves(pos, direction, walls):
                new_key = new_pos, new_direction
                new_cost = before_cost + cost
                if new_key not in all_distances or new_cost < all_distances[new_key]:
                    all_distances[new_key] = new_cost
                    new_keys.add(new_key)
        next_keys = new_keys
    #print(all_distances)
    best_cost = min(cost for (pos, _), cost in all_distances.items() if pos == end)
    #print(best_cost)
    return best_cost

assert solve1(EXAMPLE) == 7036
assert solve1(EXAMPLE2) == 11048

def solve2(data):
    walls, start, end = parse(data)
    start_key = start, (1, 0)
    all_distances = {start_key: (0, [])}
    next_keys = {start_key}
    while next_keys:
        #print(len(next_keys), len(all_distances))
        new_keys = set()
        for old_key in next_keys:
            pos, direction = old_key
            before_cost = all_distances[(pos, direction)][0]
            for new_pos, new_direction, cost in enumerate_moves(pos, direction, walls):
                new_key = new_pos, new_direction
                new_cost = before_cost + cost
                if new_key not in all_distances or new_cost < all_distances[new_key][0]:
                    # new path or cheaper path found, create or overwrite
                    all_distances[new_key] = (new_cost, [old_key])
                    new_keys.add(new_key)
                elif new_key in all_distances and new_cost == all_distances[new_key][0]:
                    # found an equally good path, update
                    existing_paths = all_distances[new_key][1]
                    assert len(existing_paths) > 0 and old_key not in existing_paths
                    existing_paths.append(old_key)
        next_keys = new_keys
    #print(all_distances)
    best_cost = min(cost for (pos, _), (cost, _) in all_distances.items() if pos == end)
    end_keys = [(pos, direction) for (pos, direction), (cost, _) in all_distances.items() if pos == end and cost == best_cost]
    # use stored paths to search backwards from the end
    assert len(end_keys) > 0
    next_keys = set(end_keys)
    all_path_keys = set(end_keys)
    while next_keys:
        new_keys = set()
        for key in next_keys:
            assert key in all_distances
            _, paths = all_distances[key]
            for new_key in paths:
                if new_key not in all_path_keys:
                    all_path_keys.add(new_key)
                    new_keys.add(new_key)
        next_keys = new_keys
    all_positions = {pos for pos, _ in all_path_keys}
    return len(all_positions)

assert solve2(EXAMPLE) == 45
assert solve2(EXAMPLE2) == 64

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
