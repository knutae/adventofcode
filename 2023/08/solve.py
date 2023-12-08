EXAMPLE1 = '''
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
'''

EXAMPLE2 = '''
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
'''

def parse_node(line):
    lhs, rhs = line.split(' = ')
    rhs = rhs[1:-1].split(', ')
    return lhs, tuple(rhs)

def parse(data):
    moves, rest = data.strip().split('\n\n')
    moves = ['LR'.index(x) for x in moves]
    network = dict(parse_node(line) for line in rest.split('\n'))
    return moves, network

def solve1(data):
    moves, network = parse(data)
    node = 'AAA'
    count = 0
    while node != 'ZZZ':
        move = moves[count % len(moves)]
        node = network[node][move]
        count += 1
    return count

assert solve1(EXAMPLE1) == 2
assert solve1(EXAMPLE2) == 6

with open('input') as f:
    data = f.read()

print(solve1(data))
