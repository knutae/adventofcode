from bisect import bisect_left
from functools import cache

EXAMPLE = '''
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
'''

def parse(data):
    patterns, designs = data.strip().split('\n\n')
    patterns = patterns.split(', ')
    designs = designs.split('\n')
    patterns.sort()
    return patterns, designs


def can_make_design(patterns, design):
    assert len(design) > 0
    ip = bisect_left(patterns, design[0])
    while ip < len(patterns) and patterns[ip][0] == design[0]:
        if patterns[ip] == design:
            return True
        if design.startswith(patterns[ip]) and can_make_design(patterns, design[len(patterns[ip]):]):
            return True
        ip += 1
    return False

@cache
def count_ways_to_make_design(patterns, design):
    assert len(design) > 0
    ip = bisect_left(patterns, design[0])
    solutions = 0
    while ip < len(patterns) and patterns[ip][0] == design[0]:
        if patterns[ip] == design:
            solutions += 1
        elif design.startswith(patterns[ip]):
            solutions += count_ways_to_make_design(patterns, design[len(patterns[ip]):])
        ip += 1
    return solutions

def solve1(data):
    patterns, designs = parse(data)
    return sum(1 for d in designs if can_make_design(patterns, d))

def solve2(data):
    patterns, designs = parse(data)
    patterns = tuple(patterns)
    return sum(count_ways_to_make_design(patterns, d) for d in designs)

assert solve1(EXAMPLE) == 6
assert solve2(EXAMPLE) == 16

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
