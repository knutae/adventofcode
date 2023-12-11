from itertools import combinations

EXAMPLE = '''
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
'''

def parse(data):
    grid = data.strip().split('\n')
    galaxies = set()
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == '#':
                galaxies.add((x,y))
    return galaxies

def expand_1d_map(coord, expand_amount=2):
    mapping = {}
    add = 0
    for c in range(max(coord) + 1):
        if c in coord:
            mapping[c] = c + add
        else:
            add += (expand_amount - 1)
    return mapping

def expand(galaxies, expand_amount=2):
    cols = {x for x,_ in galaxies}
    rows = {y for _,y in galaxies}
    col_map = expand_1d_map(cols, expand_amount)
    row_map = expand_1d_map(rows, expand_amount)
    return {(col_map[x], row_map[y]) for x,y in galaxies}

def print_galaxies(galaxies):
    w = max(x for x,_ in galaxies) + 1
    for y in range(0, max(y for _,y in galaxies) + 1):
        print(''.join('*' if (x,y) in galaxies else '.' for x in range(w)))            

#print_galaxies(expand(parse(EXAMPLE)))

def distance(g1, g2):
    return sum(abs(a-b) for a,b in zip(g1, g2))

def solve1(data):
    galaxies = parse(data)
    galaxies = expand(galaxies)
    return sum(distance(a,b) for a, b in combinations(galaxies, 2))

assert solve1(EXAMPLE) == 374

def solve2(data, expand_amount=1000000):
    galaxies = parse(data)
    galaxies = expand(galaxies, expand_amount)
    result = sum(distance(a,b) for a, b in combinations(galaxies, 2))
    #print(expand_amount, result)
    return result

assert solve2(EXAMPLE, 10) == 1030
assert solve2(EXAMPLE, 100) == 8410

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
