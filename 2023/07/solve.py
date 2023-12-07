EXAMPLE = '''
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''

CARDS = '23456789TJQKA'

def parse_line(line):
    a, b = line.split()
    return a, int(b)

def parse(data):
    return [parse_line(line) for line in data.strip().split('\n')]

def hand_type(hand):
    counts = list(sorted({c: hand.count(c) for c in hand}.values()))
    if counts == [5]:
        # five of a kind
        return 6
    if counts == [1, 4]:
        # four of a kind
        return 5
    if counts == [2, 3]:
        # full house
        return 4
    if counts == [1, 1, 3]:
        # three of a kind
        return 3
    if counts == [1, 2, 2]:
        # two pair
        return 2
    if counts == [1, 1, 1, 2]:
        # one pair
        return 1
    if counts == [1, 1, 1, 1, 1]:
        # high card
        return 0
    assert False

def hand_key(hand):
    return hand_type(hand), tuple(CARDS.index(c) for c in hand)

def solve1(data):
    hands_and_bids = parse(data)
    hands_and_bids.sort(key = lambda x: hand_key(x[0]))
    result = 0
    for i, item in enumerate(hands_and_bids):
        _, bid = item
        result += (i + 1) * bid
        #print((i + 1), hand, bid, (i + 1) * bid)
    return result

def hand_type_with_jokers(hand):
    if 'J' not in hand:
        return hand_type(hand)
    joker_count = hand.count('J')
    counts = list(sorted({c: hand.count(c) for c in hand if c != 'J'}.values()))
    if len(counts) <= 1:
        # five of a kind
        return 6
    if len(counts) == 2:
        # with two kinds of non-jokers, we can always do four of a kind or full house
        if 1 in counts:
            # four of a kind
            return 5
        else:
            # full house
            return 4
    if len(counts) == 3:
        # as seen by asserts below, this will always give three of a kind
        assert max(counts) <= 2
        assert joker_count <= 2
        if 2 in counts:
            assert counts == [1, 1, 2] and joker_count == 1
        else:
            assert counts == [1, 1, 1] and joker_count == 2
        return 3
    if len(counts) == 4:
        assert counts == [1, 1, 1, 1] and joker_count == 1
        # one pair
        return 1
    assert False

JOKER_CARDS = 'J23456789TQKA'

def hand_key_with_jokers(hand):
    return hand_type_with_jokers(hand), tuple(JOKER_CARDS.index(c) for c in hand)

def solve2(data):
    hands_and_bids = parse(data)
    hands_and_bids.sort(key = lambda x: hand_key_with_jokers(x[0]))
    result = 0
    for i, item in enumerate(hands_and_bids):
        _, bid = item
        result += (i + 1) * bid
        #print((i + 1), hand, bid, (i + 1) * bid)
    return result

assert solve1(EXAMPLE) == 6440
assert solve2(EXAMPLE) == 5905

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
