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

def highest_joltage(bank, n):
    result = []
    for i in range(n):
        if i == n-1:
            # last
            c = max(bank)
        else:
            c = max(bank[:-n + i + 1])
            index = bank.index(c)
            bank = bank[index+1:]
        result.append(c)
    return int(''.join(str(c) for c in result))

def solve1(s):
    return sum(highest_joltage(bank, 2) for bank in parse(s))

assert solve1(EXAMPLE) == 357

def solve2(s):
    return sum(highest_joltage(bank, 12) for bank in parse(s))

assert solve2(EXAMPLE) == 3121910778619

with open('input') as f:
    s = f.read()

print(solve1(s))
print(solve2(s))
