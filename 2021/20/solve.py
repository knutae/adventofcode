EXAMPLE = '''
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
'''

def parse(data):
    table, image_data = data.strip().split('\n\n')
    table = table.replace('\n', '') # for the example
    assert len(table) == 512
    lines = image_data.split('\n')
    pixels = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            assert c in '#.'
            if c == '#':
                pixels.add((x,y))
    return table, pixels

def pixel_ranges(pixels):
    x_range = range(min(p[0] for p in pixels)-1, max(p[0] for p in pixels)+2)
    y_range = range(min(p[1] for p in pixels)-1, max(p[1] for p in pixels)+2)
    return x_range, y_range

def print_image(pixels, inverted):
    x_range, y_range = pixel_ranges(pixels)
    for y in y_range:
        if inverted:
            print(''.join('.' if (x,y) in pixels else '#' for x in x_range))
        else:
            print(''.join('#' if (x,y) in pixels else '.' for x in x_range))

def bin_digit(pixels, x, y, inverted):
    if inverted:
        return '0' if (x,y) in pixels else '1'
    else:
        return '1' if (x,y) in pixels else '0'

def square_around(x, y):
    for y0 in range(y-1, y+2):
        for x0 in range(x-1, x+2):
            yield x0,y0

def table_index(pixels, x, y, inverted):
    # could avoid going via a string here
    bin_number = ''.join(bin_digit(pixels, x0, y0, inverted) for x0, y0 in square_around(x, y))
    return int(bin_number, 2)

def step(table, pixels, inverted):
    x_range, y_range = pixel_ranges(pixels)
    if table[0] == '.':
        assert not inverted
        return {(x,y) for x in x_range for y in y_range if table[table_index(pixels, x, y, inverted)] == '#'}, False
    else:
        if inverted:
            # return non-inverted pixels from inverted pixels
            return {(x,y) for x in x_range for y in y_range if table[table_index(pixels, x, y, inverted)] == '#'}, False
        else:
            # return inverted pixels from non-inverted pixels
            return {(x,y) for x in x_range for y in y_range if table[table_index(pixels, x, y, inverted)] == '.'}, True

def solve(data, enhancement_count):
    table, pixels = parse(data)
    inverted = False
    for _ in range(enhancement_count):
        old_len = len(pixels)
        pixels, inverted = step(table, pixels, inverted)
        #print_image(pixels, inverted)
        #print(f'{old_len} -> {len(pixels)} ({"inverted" if inverted else "normal"})\n')
    return len(pixels)

def solve1(data):
    return solve(data, 2)

def solve2(data):
    return solve(data, 50)

assert solve1(EXAMPLE) == 35
assert solve2(EXAMPLE) == 3351

with open('input') as f:
    puzzle_input = f.read()

print(solve1(puzzle_input))
print(solve2(puzzle_input))
