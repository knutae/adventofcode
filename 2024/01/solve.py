from collections import Counter

EXAMPLE = '''
3   4
4   3
2   5
1   3
3   9
3   3
'''

def parse(data):
    lines = data.strip().split('\n')
    return [
        tuple(int(x) for x in line.split())
        for line in lines
    ]

def solve1(data):
    pairs = parse(data)
    sorted_a = sorted(x[0] for x in pairs)
    sorted_b = sorted(x[1] for x in pairs)
    r = 0
    for a, b in zip(sorted_a, sorted_b):
        r += abs(a-b)
    return r

def solve2(data):
    tuples = parse(data)
    a = [x[0] for x in tuples]
    b = [x[1] for x in tuples]
    c = Counter(b)
    score = 0
    for n in a:
        score += n * c.get(n, 0)
    return score

assert solve1(EXAMPLE) == 11
assert solve2(EXAMPLE) == 31

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
