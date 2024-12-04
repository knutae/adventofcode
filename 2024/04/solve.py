EXAMPLE = '''
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
'''

def parse(data):
    return data.strip().split('\n')

def columns(lines):
    height = len(lines)
    width = len(lines[0])
    return [''.join(lines[y][x] for y in range(height)) for x in range(width)]

def diagonals_up(lines):
    height = len(lines)
    width = len(lines[0])
    r = []
    for start_y in range(height*2):
        r.append(
            ''.join(
                lines[start_y - x][x]
                for x in range(width)
                if (start_y - x) in range(height)))
    return [line for line in r if len(line) >= 4]

def diagonals_down(lines):
    height = len(lines)
    width = len(lines[0])
    r = []
    for start_y in range(-height, height):
        r.append(
            ''.join(
                lines[start_y + x][x]
                for x in range(width)
                if (start_y + x) in range(height)))
    return [line for line in r if len(line) >= 4]

def count_xmas(lines):
    return sum(line.count('XMAS') + line.count('SAMX') for line in lines)

def solve1(data):
    lines = parse(data)
    return (
        count_xmas(lines)
        + count_xmas(columns(lines))
        + count_xmas(diagonals_up(lines))
        + count_xmas(diagonals_down(lines))
    )

assert solve1(EXAMPLE) == 18

with open('input') as f:
    data = f.read()

print(solve1(data))
