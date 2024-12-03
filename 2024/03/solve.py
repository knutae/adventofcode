import re

EXAMPLE = '''
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
'''

EXAMPLE2 = '''
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
'''

def solve1(data):
    pattern = re.compile(r'mul\(([0-9]+),([0-9]+)\)')
    r = 0
    for m in pattern.finditer(data):
        r += int(m.group(1)) * int(m.group(2))
    return r

def solve2(data):
    pattern = re.compile(r"mul\(([0-9]+),([0-9]+)\)|do\(\)|don't\(\)")
    enabled = True
    r = 0
    for m in pattern.finditer(data):
        if m.group(0) == 'do()':
            enabled = True
        elif m.group(0) == "don't()":
            enabled = False
        elif enabled:
            r += int(m.group(1)) * int(m.group(2))
    return r

assert solve1(EXAMPLE) == 161
assert solve2(EXAMPLE2) == 48

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
