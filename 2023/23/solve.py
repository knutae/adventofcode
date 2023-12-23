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

def generate_moves2(grid, pos):
    x, y = pos
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        px, py = x+dx, y+dy
        if py >= 0 and py < len(grid) and grid[py][px] != '#':
            yield px, py

def all_reachable(grid, pos, visited):
    # find all reachable positions from the given position
    reachable = set()
    current_positions = [pos]
    while current_positions:
        next_positions = []
        for a in current_positions:
            for b in generate_moves2(grid, a):
                if b not in reachable and b not in visited:
                    reachable.add(b)
                    next_positions.append(b)
        current_positions = next_positions
    return reachable

def longest_path2(grid, pos, dest, visited, best):
    reachable = all_reachable(grid, pos, visited)
    if dest not in reachable:
        # no path to destination
        return None
    elif best:
        assert len(best) == 1
        if len(visited) + len(reachable) <= best[0]:
            # best path is already as long than the upper limit of what is possible, abort early
            return None
    visited = set(visited) | {pos}
    moves = [p for p in generate_moves2(grid, pos) if p not in visited]
    while len(moves) == 1:
        # avoid recursion if there's only one path
        pos = moves[0]
        visited.add(pos)
        moves = [p for p in generate_moves2(grid, pos) if p not in visited]
    if len(moves) == 0:
        if pos != dest:
            # dead end, not at dest
            return None
        #print(f'Solution {len(visited)} vs previous best {best}')
        if len(best) == 0:
            best.append(len(visited))
        elif len(visited) > best[0]:
            best[0] = len(visited)
        return visited
    # at a fork: recursively find the longest path
    assert len(moves) in (2,3)
    paths = [longest_path2(grid, p, dest, visited, best) for p in moves]
    paths = [path for path in paths if path is not None]
    if len(paths) == 0:
        # all paths from the fork were dead ends or aborted
        return None
    return max(paths, key=len)

def solve2(data):
    grid, start, dest = parse(data)
    path = longest_path2(grid, start, dest, set(), [])
    return len(path) - 1

assert solve2(EXAMPLE) == 154

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
