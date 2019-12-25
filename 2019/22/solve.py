import math
import sys
import time

def deal_into_new_stack(cards):
    return cards[::-1]

def cut_cards(cards, n):
    return cards[n:] + cards[:n]

def deal_with_increment(cards, n):
    r = [None]*len(cards)
    for i, c in enumerate(cards):
        r[i*n % len(cards)] = c
    return r

def run_command(cards, command):
    if command == 'deal into new stack':
        return deal_into_new_stack(cards)
    if command.startswith('cut '):
        n = int(command[len('cut '):])
        return cut_cards(cards, n)
    if command.startswith('deal with increment '):
        n = int(command[len('deal with increment '):])
        return deal_with_increment(cards, n)
    assert False

def shuffle(cards, commands):
    for command in commands:
        cards = run_command(cards, command)
    return cards

# modular division, sources:
# https://www.geeksforgeeks.org/modular-division/
# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
def extended_gcd(a, b):
    s = 0
    old_s = 1
    t = 1
    old_t = 0
    r = b
    old_r = a
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_r, old_s, old_t

def modular_inverse(b, m):
    g, x, _ = extended_gcd(b, m)
    assert g == 1
    return x % m

def modular_divide(a, b, m):
    a = a % m
    inv = modular_inverse(b, m)
    assert inv >= 0
    return (inv * a) % m

def circular_div(length, pos, divident):
    assert pos < length
    div = modular_divide(pos, divident, length)
    #print(f'circular_div{(pos, divident, length)} -> {div}, inverse {modular_inverse(divident, length)}')
    return div

class Command:
    def __init__(self, length, cut, increment):
        assert length > 0
        assert cut >= 0 and cut < length
        assert increment > 0 and increment < length
        self.length = length
        self.cut = cut
        self.increment = increment

    def convert_position(self, position):
        position = (position + self.cut) % self.length
        position = circular_div(self.length, position, self.increment)
        return position

    def __repr__(self):
        return f'Command(length={self.length}, cut={self.cut}, increment={self.increment})'

def parse_command(command, length):
    if command == 'deal into new stack':
        return Command(length, 1, length-1)
    if command.startswith('cut '):
        n = int(command[len('cut '):]) % length
        return Command(length, n, 1)
    if command.startswith('deal with increment '):
        n = int(command[len('deal with increment '):])
        return Command(length, 0, n)
    assert False

def merge_commands(a: Command, b: Command):
    assert a.length == b.length
    cut = (a.cut + b.cut * a.increment) % a.length
    increment = (a.increment * b.increment) % a.length
    #print(f'merge ({a.cut} {a.increment}) ({b.cut} {b.increment}) -> ({cut} {increment})')
    return Command(a.length, cut, increment)

def merge_repeated(command: Command, repetitions: int):
    assert repetitions > 0
    if repetitions == 1:
        return command
    half = merge_repeated(command, repetitions // 2)
    full = merge_commands(half, half)
    if repetitions % 2 == 1:
        full = merge_commands(full, command)
    return full

def lazy_index_of(commands, position, iterations=1, verbose=False):
    commands = list(reversed(commands))
    cmd = Command(commands[0].length, 0, 1)
    for c in commands:
        cmd = merge_commands(cmd, c)
    #print(f'Phase 1: {cmd}')
    cmd = merge_repeated(cmd, iterations)
    #print(f'Phase 2: {cmd}')
    position = cmd.convert_position(position)
    #for _ in range(iterations):
    #    position = cmd.convert_position(position)
    return position

def test():
    cards = [0,1,2,3,4,5,6,7,8,9]
    assert cut_cards(cards, 3) == [3,4,5,6,7,8,9,0,1,2]
    assert cut_cards(cards, -4) == [6,7,8,9,0,1,2,3,4,5]
    assert deal_with_increment(cards, 3) == [0,7,4,1,8,5,2,9,6,3]
    assert shuffle(cards, [
        'deal with increment 7',
        'deal into new stack',
        'deal into new stack',
    ]) == [0,3,6,9,2,5,8,1,4,7]
    assert shuffle(cards, [
        'cut 6',
        'deal with increment 7',
        'deal into new stack',
    ]) == [3,0,7,4,1,8,5,2,9,6]
    assert shuffle(cards, [
        'deal with increment 7',
        'deal with increment 9',
        'cut -2',
    ]) == [6,3,0,7,4,1,8,5,2,9]
    assert shuffle(cards, [
        'deal into new stack',
        'cut -2',
        'deal with increment 7',
        'cut 8',
        'cut -4',
        'deal with increment 7',
        'cut 3',
        'deal with increment 9',
        'deal with increment 3',
        'cut -1',
    ]) == [9,2,5,8,1,4,7,0,3,6]

def test_command(command: Command, expected_result):
    actual = [command.convert_position(i) for i in range(10)]
    if actual != expected_result:
        print(f'Expected {expected_result}, got {actual}')
        assert False

def test_lazy_shuffle(expected_result, commands):
    commands = [parse_command(s, 10) for s in commands]
    actual = [lazy_index_of(commands, i) for i in range(10)]
    if actual != expected_result:
        print(f'Expected {expected_result}, got {actual}')
        assert False

def test_circular_div(expected_result, divisor):
    length = len(expected_result)
    actual = [circular_div(length, i, divisor) for i in range(length)]
    if actual != expected_result:
        print(f'Expected {expected_result}, got {actual}')
        assert False

def test_lazy():
    # length 10
    test_circular_div([0,1,2,3,4,5,6,7,8,9], 1) # 1 -> 1
    test_circular_div([0,7,4,1,8,5,2,9,6,3], 3) # 3 -> 7
    test_circular_div([0,3,6,9,2,5,8,1,4,7], 7) # 7 -> 3
    test_circular_div([0,9,8,7,6,5,4,3,2,1], 9) # 9 -> 9
    # length 11
    test_circular_div([0,1,2,3,4,5,6,7,8,9,10], 1) # 1 -> 1
    test_circular_div([0,6,1,7,2,8,3,9,4,10,5], 2) # 2 -> 6
    test_circular_div([0,4,8,1,5,9,2,6,10,3,7], 3) # 3 -> 4
    test_circular_div([0,3,6,9,1,4,7,10,2,5,8], 4) # 4 -> 3
    test_circular_div([0,9,7,5,3,1,10,8,6,4,2], 5) # 5 -> 9
    test_circular_div([0,2,4,6,8,10,1,3,5,7,9], 6) # 6 -> 2
    test_circular_div([0,8,5,2,10,7,4,1,9,6,3], 7) # 7 -> 8
    test_circular_div([0,7,3,10,6,2,9,5,1,8,4], 8) # 8 -> 7
    test_circular_div([0,5,10,4,9,3,8,2,7,1,6], 9) # 9 -> 5
    test_circular_div([0,10,9,8,7,6,5,4,3,2,1], 10) # 10 -> 10
    #test_circular_div([ , , , , , , , , , , ],  )
    #test_command(parse_command('deal into new stack', 10), [9,8,7,6,5,4,3,2,1,0])
    test_command(parse_command('cut 3', 10), [3,4,5,6,7,8,9,0,1,2])
    test_command(parse_command('cut -4', 10), [6,7,8,9,0,1,2,3,4,5])
    test_command(parse_command('deal with increment 3', 10), [0,7,4,1,8,5,2,9,6,3])
    test_lazy_shuffle([9,8,7,6,5,4,3,2,1,0], [
        'deal into new stack',
    ])
    test_lazy_shuffle([0,1,2,3,4,5,6,7,8,9], [
        'deal into new stack',
        'deal into new stack',
    ])
    test_lazy_shuffle([0,3,6,9,2,5,8,1,4,7], [
        'deal with increment 7',
        'deal into new stack',
        'deal into new stack',
    ])
    test_lazy_shuffle([3,0,7,4,1,8,5,2,9,6], [
        'cut 6',
        'deal with increment 7',
        'deal into new stack',
    ])
    test_lazy_shuffle([6,3,0,7,4,1,8,5,2,9], [
        'deal with increment 7',
        'deal with increment 9',
        'cut -2',
    ])
    test_lazy_shuffle([9,2,5,8,1,4,7,0,3,6], [
        'deal into new stack',
        'cut -2',
        'deal with increment 7',
        'cut 8',
        'cut -4',
        'deal with increment 7',
        'cut 3',
        'deal with increment 9',
        'deal with increment 3',
        'cut -1',
    ])

test()
test_lazy()

def main():
    cards = list(range(10007))
    with open('input') as f:
        commands = f.read().strip().split('\n')
    cards = shuffle(cards, commands)
    print(cards.index(2019))

def main_lazy():
    with open('input') as f:
        commands = f.read().strip().split('\n')
    length = 119315717514047
    commands = [parse_command(s, length) for s in commands]
    result = lazy_index_of(commands, 2020, iterations=101741582076661, verbose=True)
    print(result)

#main()
main_lazy()
