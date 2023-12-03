EXAMPLE = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def parse(data):
    lines = data.strip().split("\n")
    numbers = {}
    symbols = {}
    for y, line in enumerate(lines):
        current_number = 0
        for x, c in enumerate(line):
            if c.isdigit():
                current_number = current_number * 10 + int(c)
            elif current_number > 0:
                number_length = len(str(current_number))
                numbers[(x - number_length, y)] = current_number
                current_number = 0
            if not c.isdigit() and c != ".":
                symbols[(x, y)] = c
        if current_number > 0:
            number_length = len(str(current_number))
            numbers[(len(line) - number_length, y)] = current_number
    return numbers, symbols


def is_adjacent(number, number_pos, symbol_pos):
    number_length = len(str(number))
    nx, ny = number_pos
    sx, sy = symbol_pos
    if abs(sy - ny) > 1:
        return False
    return sx >= nx - 1 and sx <= nx + number_length


def solve1(data):
    numbers, symbols = parse(data)
    r = 0
    for number_pos, number in numbers.items():
        if any(is_adjacent(number, number_pos, symbol_pos) for symbol_pos in symbols):
            r += number
    return r


assert solve1(EXAMPLE) == 4361

with open("input") as f:
    data = f.read()

print(solve1(data))
