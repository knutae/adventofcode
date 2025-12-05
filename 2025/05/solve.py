EXAMPLE = '''
3-5
10-14
16-20
12-18

1
5
8
11
17
32
'''

def parse_range(s):
    a, b = [int(x) for x in s.split('-')]
    return range(a, b+1)

def parse(s):
    ranges, ids = s.strip().split('\n\n')
    ranges = [parse_range(line) for line in ranges.split('\n')]
    ids = [int(line) for line in ids.split('\n')]
    return ranges, ids

def solve1(s):
    ranges, ids = parse(s)
    return sum(1 for id in ids if any(id in r for r in ranges))

assert solve1(EXAMPLE) == 3

with open('input') as f:
    s = f.read()

print(solve1(s))
