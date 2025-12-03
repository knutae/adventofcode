EXAMPLE = '''
987654321111111
811111111111119
234234234234278
818181911112111
'''

def parse(s):
    return [
        [int(c) for c in line]
        for line in s.strip().split('\n')
    ]

def highest_joltage(bank):
    first = max(bank[:-1])
    second = max(bank[bank.index(first)+1:])
    return 10*first + second

def solve1(s):
    return sum(highest_joltage(bank) for bank in parse(s))

assert solve1(EXAMPLE) == 357

with open('input') as f:
    s = f.read()

print(solve1(s))
