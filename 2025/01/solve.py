EXAMPLE = '''
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
'''

def parse(s):
    def parse_line(line):
        if line.startswith('L'):
            return -int(line[1:])
        else:
            return int(line[1:])
    return [parse_line(line) for line in s.strip().split('\n')]

def solve1(s):
    dial = 50
    c = 0
    for n in parse(s):
        dial = (dial + n) % 100
        if dial == 0:
            c += 1
    return c

assert solve1(EXAMPLE) == 3

def solve2(s):
    dial = 50
    c = 0
    for n in parse(s):
        if n > 0:
            dist_to_zero = 100 - dial
        else:
            assert n < 0
            dist_to_zero = 100 if dial == 0 else dial
        if abs(n) >= dist_to_zero:
            c += 1 + (abs(n) - dist_to_zero) // 100
        dial = (dial + n) % 100
    return c

assert solve2(EXAMPLE) == 6

with open('input') as f:
    s = f.read()

print(solve1(s))
print(solve2(s))
