EXAMPLE = '''
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
'''

def parse(data):
    lines = data.strip().split('\n')
    height = len(lines)
    width = len(lines[0])
    east = set()
    south = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '>':
                east.add((x,y))
            elif c == 'v':
                south.add((x,y))
            else:
                assert c == '.'
    return width, height, east, south

#print(parse(EXAMPLE))

def step(width, height, east, south):
    new_east = set()
    for x,y in east:
        new_pos = (x+1) % width, y
        if new_pos in east or new_pos in south:
            new_pos = x,y
        new_east.add(new_pos)
    east = new_east
    new_south = set()
    for x,y in south:
        new_pos = x, (y+1) % height
        if new_pos in east or new_pos in south:
            new_pos = x,y
        new_south.add(new_pos)
    return new_east, new_south

def solve1(data):
    width, height, east, south = parse(data)
    steps = 0
    while True:
        steps += 1
        new_east, new_south = step(width, height, east, south)
        if (new_east, new_south) == (east, south):
            break
        east, south = new_east, new_south
    return steps

assert solve1(EXAMPLE) == 58

with open('input') as f:
    puzzle_input = f.read()

print(solve1(puzzle_input))
