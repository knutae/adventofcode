TEST_INPUT = '''
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
'''

def parse(input):
    return input.strip().split('\n')

def count_trees(area, right, down):
    width = len(area[0])
    height = len(area)
    x = 0
    y = 0
    trees = 0
    while y < height:
        if area[y][x] == '#':
            trees += 1
        x = (x + right) % width
        y += down
    #print(right, down, trees)
    return trees

def solve1(area):
    return count_trees(area, 3, 1)

def multiply_slopes(area, slopes):
    product = 1
    for right, down in slopes:
        product *= count_trees(area, right, down)
    return product

def solve2(area):
    return multiply_slopes(area, [(1,1), (3,1), (5,1), (7,1), (1,2)])

area = parse(TEST_INPUT)
assert solve1(area) == 7
assert count_trees(area, 1, 1) == 2
assert count_trees(area, 3, 1) == 7
assert count_trees(area, 5, 1) == 3
assert count_trees(area, 7, 1) == 4
assert count_trees(area, 1, 2) == 2
assert solve2(area) == 336

with open('input') as f:
    area = parse(f.read())
print(solve1(area))
print(solve2(area))
