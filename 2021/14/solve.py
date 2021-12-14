from collections import Counter

EXAMPLE='''
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
'''

def parse_rule(line):
    a,b,c = line.split()
    assert b == '->'
    return a,c

def parse(data):
    start, rules = data.strip().split('\n\n')
    rules = dict(parse_rule(line) for line in rules.split('\n'))
    return start, rules

def step(polymer, rules):
    result = [polymer[0]]
    for i in range(1, len(polymer)):
        result.append(rules[polymer[i-1:i+1]])
        result.append(polymer[i])
    return ''.join(result)

def solve1(data, steps=10):
    polymer, rules = parse(data)
    for _ in range(steps):
        polymer = step(polymer, rules)
    c = Counter(polymer)
    return max(c.values()) - min(c.values())

def test():
    polymer, rules = parse(EXAMPLE)
    polymer = step(polymer, rules)
    assert polymer == 'NCNBCHB'
    polymer = step(polymer, rules)
    assert polymer == 'NBCCNBBBCBHCB'
    polymer = step(polymer, rules)
    assert polymer == 'NBBBCNCCNBBNBNBBCHBHHBCHB'
    polymer = step(polymer, rules)
    assert polymer == 'NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB'

test()

assert solve1(EXAMPLE) == 1588

def step_counts(counts, rules):
    new_counts = Counter()
    for pair, count in counts.items():
        a,b = pair
        c = rules[pair]
        new_counts[a+c] += count
        new_counts[c+b] += count
    return new_counts

def solve2(data, steps=40):
    polymer, rules = parse(data)
    counts = Counter()
    for a,b in zip(polymer, polymer[1:]):
        counts[a+b] += 1
    for i in range(steps):
        counts = step_counts(counts, rules)
    letter_counts = Counter()
    for pair, count in counts.items():
        letter_counts[pair[0]] += count
    letter_counts[polymer[-1]] += 1 # fix last letter count
    return max(letter_counts.values()) - min(letter_counts.values())

assert solve2(EXAMPLE, 10) == 1588
assert solve2(EXAMPLE) == 2188189693529

with open('input') as f:
    puzzle_input = f.read()

print(solve1(puzzle_input))
print(solve2(puzzle_input))
