EXAMPLE = '''
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''

def parse_line(line):
    return [int(x) for x in line.split()]

def parse(data):
    return [parse_line(line) for line in data.strip().split('\n')]

def predict_next(sequence):
    if all(x == 0 for x in sequence):
        return 0
    diffs = [b-a for a, b in zip(sequence, sequence[1:])]
    #print(sequence, diffs)
    return sequence[-1] + predict_next(diffs)

def solve1(data):
    lines = parse(data)
    return sum(predict_next(line) for line in lines)

def predict_previous(sequence):
    if all(x == 0 for x in sequence):
        return 0
    diffs = [b-a for a, b in zip(sequence, sequence[1:])]
    #print(sequence, diffs)
    return sequence[0] - predict_previous(diffs)

def solve2(data):
    lines = parse(data)
    return sum(predict_previous(line) for line in lines)

assert solve1(EXAMPLE) == 114
assert solve2(EXAMPLE) == 2

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
