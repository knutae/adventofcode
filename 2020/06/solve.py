def solve1(input):
    groups = input.strip().split('\n\n')
    return sum(len(set(x.replace('\n',''))) for x in groups)

EXAMPLE = '''
abc

a
b
c

ab
ac

a
a
a
a

b'''

assert solve1(EXAMPLE) == 11

def intersection_size(answers):
    return len(set.intersection(*map(set, answers)))

def solve2(input):
    groups = input.strip().split('\n\n')
    return sum(intersection_size(x.split('\n')) for x in groups)

assert solve2(EXAMPLE) == 6

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
