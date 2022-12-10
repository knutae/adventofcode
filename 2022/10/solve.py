SMALL_EXAMPLE = '''
noop
addx 3
addx -5
'''

BIG_EXAMPLE = '''
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
'''

def parse_line(line):
    if line == 'noop':
        return None
    [cmd, n] = line.split()
    assert cmd == 'addx'
    return int(n)

def parse(input):
    return [parse_line(line) for line in input.strip().split('\n')]

def solve1(input):
    timeline = [1]
    for n in parse(input):
        x = timeline[-1]
        if n is None:
            timeline.append(x)
        else:
            timeline.append(x)
            timeline.append(x + n)
    return sum(i*timeline[i-1] for i in range(20,len(timeline)+1,40))

def solve2(input):
    timeline = [1]
    for n in parse(input):
        x = timeline[-1]
        if n is None:
            timeline.append(x)
        else:
            timeline.append(x)
            timeline.append(x + n)
    screen = []
    for cycle, x in enumerate(timeline[:-1]):
        pos = cycle % 40
        screen.append('#' if abs(pos - x) <= 1 else '.')
        if pos == 39:
            screen.append('\n')
    return ''.join(screen)

solve1(SMALL_EXAMPLE)
assert solve1(BIG_EXAMPLE) == 13140
print(solve2(BIG_EXAMPLE))

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
