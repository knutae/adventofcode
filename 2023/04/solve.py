EXAMPLE = '''
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
'''

def parse_card(line):
    name, rest = line.split(': ')
    winning, mine = rest.split(' | ')
    winning = [int(x) for x in winning.split()]
    mine = [int(x) for x in mine.split()]
    return name, winning, mine

def parse(data):
    return [parse_card(line) for line in data.strip().split('\n')]

#print(parse(EXAMPLE))

def solve1(data):
    cards = parse(data)
    r = 0
    for _, winning, mine in cards:
        score = 0
        for c in mine:
            if c in winning:
                score = score * 2 if score > 0 else 1
        r += score
    return r

assert solve1(EXAMPLE) == 13

with open('input') as f:
    data = f.read()

print(solve1(data))
