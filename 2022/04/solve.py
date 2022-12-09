EXAMPLE_INPUT = '''
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''

def parse_range(r):
    [a, b] = r.split('-')
    return int(a), int(b)

def parse_line(line):
    [a, b] = line.split(',')
    return parse_range(a), parse_range(b)

def parse(input):
    return [parse_line(line) for line in input.strip().split('\n')]

def range_contains(larger, smaller):
    return larger[0] <= smaller[0] and larger[1] >= smaller[1]

def solve1(input):
    return sum(1 for a, b in parse(input) if range_contains(a, b) or range_contains(b, a))

def overlaps(a, b):
    return (a[0] <= b[0] and b[0] <= a[1]) or (a[0] <= b[1] and b[1] <= a[1]) or range_contains(b, a)

def solve2(input):
    return sum(1 for a, b in parse(input) if overlaps(a, b))

assert solve1(EXAMPLE_INPUT) == 2
assert solve2(EXAMPLE_INPUT) == 4

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
