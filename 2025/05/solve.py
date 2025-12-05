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

def try_join_ranges(a: range, b: range):
    if a.start > b.start:
        a, b = b, a
    if b.start > a.stop:
        # cannot join
        return None
    return range(a.start, max(a.stop, b.stop))

assert try_join_ranges(range(3,6), range(7, 9)) is None
assert try_join_ranges(range(3,6), range(6, 9)) == range(3,9)
assert try_join_ranges(range(4,9), range(2, 8)) == range(2,9)

def solve2(s):
    ranges, _ = parse(s)
    ranges.sort(key=lambda r:r.start)
    distinct_ranges = []
    current = ranges[0]
    for next in ranges[1:]:
        joined = try_join_ranges(current, next)
        if joined is None:
            distinct_ranges.append(current)
            current = next
        else:
            current = joined
    distinct_ranges.append(current)
    #print(distinct_ranges)
    return sum(len(r) for r in distinct_ranges)

assert solve2(EXAMPLE) == 14

with open('input') as f:
    s = f.read()

print(solve1(s))
print(solve2(s))
