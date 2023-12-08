import math
from dataclasses import dataclass

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

EXAMPLE3 = '''
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
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

def solve2_slow(data):
    moves, network = parse(data)
    nodes = [node for node in network.keys() if node[2] == 'A']
    count = 0
    while not all(node[2] == 'Z' for node in nodes):
        move = moves[count % len(moves)]
        for i, node in enumerate(nodes):
            nodes[i] = network[node][move]
        count += 1
    return count

@dataclass
class Period:
    start: int
    length: int

    def step_to_index(self, step):
        if step < self.start:
            return step - self.start
        else:
            return (step - self.start) % self.length

    def match_step(self, step):
        return self.step_to_index(step) == 0

    def generate_steps(self):
        step = self.start
        while True:
            yield step
            step += self.length

def combine_periods(p1, p2):
    new_length = math.lcm(p1.length, p2.length)
    # There might be a faster way to do the following...?
    # Make sure p1 has the largest length, since we should find a match in less than p2.length iterations
    if p1.length < p2.length:
        p1, p2 = p2, p1
    for step in p1.generate_steps():
        if p2.match_step(step):
            return Period(step, new_length)

def test_combine_periods():
    assert combine_periods(Period(0, 10), Period(0, 9)) == Period(0, 90)
    assert combine_periods(Period(5, 10), Period(2, 9)) == Period(65, 90)
    assert combine_periods(Period(5, 12), Period(2, 9)) == Period(29, 36)

test_combine_periods()

def detect_period(moves, network, node):
    states = {(node, 0): 0}
    target_indexes = []
    steps = 0
    while True:
        index = steps % len(moves)
        move = moves[index]
        node = network[node][move]
        if node[2] == 'Z':
            target_indexes.append(steps + 1)
        if (node, index) in states:
            period_start = states[(node, index)]
            period_stop = steps
            period_length = period_stop - period_start
            if len(target_indexes) > 1:
                # If there is more than one target index, make some silly assertions that works with the example.
                # For the actual input, there is only one target index per starting node.
                assert period_length % len(target_indexes) == 0
                period_length = period_length // len(target_indexes)
                assert all(abs(a - b) == period_length for a, b in zip(target_indexes, target_indexes[1:]))
            target_index = min(target_indexes)
            period = Period(target_index, period_length)
            assert period.match_step(period.start)
            return period
        states[(node, index)] = steps
        steps += 1

def solve2(data):
    moves, network = parse(data)
    nodes = [node for node in network.keys() if node[2] == 'A']
    periods = [detect_period(moves, network, node) for node in nodes]
    combined_period = periods[0]
    for p in periods[1:]:
        #print("combining", combined_period, p)
        combined_period = combine_periods(combined_period, p)
    #print(combined_period)
    return combined_period.start

assert solve1(EXAMPLE1) == 2
assert solve1(EXAMPLE2) == 6
assert solve2_slow(EXAMPLE3) == 6
assert solve2(EXAMPLE3) == 6

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
