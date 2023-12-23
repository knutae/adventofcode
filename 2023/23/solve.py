EXAMPLE = '''
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
'''

def parse(data):
    grid = data.strip().split('\n')
    start = grid[0].index('.'), 0
    dest = grid[-1].index('.'), len(grid)-1
    return grid, start, dest

def generate_moves(grid, pos):
    x, y = pos
    # left
    if grid[y][x-1] in '.<':
        yield x-1, y
    # right
    if grid[y][x+1] in '.>':
        yield x+1, y
    # up
    if y > 0 and grid[y-1][x] in '.^':
        yield x, y-1
    # down
    if y < len(grid)-1 and grid[y+1][x] in '.v':
        yield x, y+1

def longest_path(grid, pos, dest, visited):
    visited = set(visited) | {pos}
    moves = [p for p in generate_moves(grid, pos) if p not in visited]
    while len(moves) == 1:
        # avoid recursion if there's only one path
        pos = moves[0]
        visited.add(pos)
        moves = [p for p in generate_moves(grid, pos) if p not in visited]
    if len(moves) == 0:
        # dead end, possibly at the destination
        return visited if pos == dest else None
    # at a fork: recursively find the longest path
    assert len(moves) in (2,3)
    paths = [longest_path(grid, p, dest, visited) for p in moves]
    paths = [path for path in paths if path is not None]
    if len(paths) == 0:
        # all paths from the fork were dead ends
        return None
    return max(paths, key=len)

def solve1(data):
    grid, start, dest = parse(data)
    path = longest_path(grid, start, dest, set())
    return len(path) - 1

assert solve1(EXAMPLE) == 94

with open('input') as f:
    data = f.read()

print(solve1(data))
