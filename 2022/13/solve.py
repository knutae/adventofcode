from functools import cmp_to_key

EXAMPLE = '''
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''

def parse_pair(pair):
    [a, b] = pair.split('\n')
    return eval(a), eval(b)

def parse(input):
    return [parse_pair(pair) for pair in input.strip().split('\n\n')]

def cmp(a, b):
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return -1
        if a == b:
            return 0
        else:
            return 1
    if isinstance(a, int):
        a = [a]
    elif isinstance(b, int):
        b = [b]
    for x, y in zip(a, b):
        r = cmp(x, y)
        if r != 0:
            return r
    return cmp(len(a), len(b))

def solve1(input):
    result = 0
    for i, pair in enumerate(parse(input)):
        a, b = pair
        if cmp(a, b) < 0:
            result += (i + 1)
    return result

def solve2(input):
    all_pairs = [eval(line) for line in input.strip().split('\n') if line]
    all_pairs.append([[2]])
    all_pairs.append([[6]])
    all_pairs.sort(key=cmp_to_key(cmp))
    #print(all_pairs)
    divider1 = all_pairs.index([[2]]) + 1
    divider2 = all_pairs.index([[6]]) + 1
    return divider1 * divider2

assert solve1(EXAMPLE) == 13
assert solve2(EXAMPLE) == 140

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
