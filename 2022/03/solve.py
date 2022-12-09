import string

TEST_INPUT = '''
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''

def split_sack(line):
    assert len(line) % 2 == 0
    half = len(line) // 2
    return line[:half], line[half:]

def parse(input):
    return [line for line in input.strip().split('\n')]

def solve1(sacks):
    result = 0
    for sack in sacks:
        a, b = split_sack(sack)
        priority = set.intersection(set(a), set(b))
        assert len(priority) == 1
        for p in priority:
            result += string.ascii_letters.index(p) + 1
    return result

def solve2(sacks):
    result = 0
    assert len(sacks) % 3 == 0
    for index in range(0, len(sacks), 3):
        group = sacks[index:index+3]
        priority = set.intersection(*map(set, group))
        assert len(priority) == 1
        for p in priority:
            result += string.ascii_letters.index(p) + 1
    return result

assert solve1(parse(TEST_INPUT)) == 157
assert solve2(parse(TEST_INPUT)) == 70

with open('input') as f:
    input = f.read()

print(solve1(parse(input)))
print(solve2(parse(input)))
