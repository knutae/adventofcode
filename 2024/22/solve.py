import itertools

EXAMPLE = '''
1
10
100
2024
'''

def parse(data):
    lines = data.strip().split('\n')
    return [int(line) for line in lines]

def mix_and_prune(a, b):
    return (a ^ b) % 16777216

def step_prandom(n):
    n = mix_and_prune(n, n * 64)
    n = mix_and_prune(n, n // 32)
    n = mix_and_prune(n, n * 2048)
    return n

assert step_prandom(123) == 15887950

def solve1(data):
    numbers = parse(data)
    r = 0
    for n in numbers:
        for _ in range(2000):
            n = step_prandom(n)
        r += n
    return r

assert solve1(EXAMPLE) == 37327623

def generate_prices(initial, length=2001):
    n = initial
    prices = []
    while len(prices) < length:
        prices.append(n % 10)
        n = step_prandom(n)
    return prices

def price_differences(prices):
    return [n-p for n, p in zip(prices[1:], prices)]

assert generate_prices(123, 10) == [3, 0, 6, 5, 4, 4, 6, 4, 4, 2]

def solve2(data, verbose=False):
    initial_numbers = parse(data)
    all_first_sequence_prices = []
    all_sequences = set()
    for initial in initial_numbers:
        prices = generate_prices(initial)
        differences = price_differences(prices)
        first_sequence_prices = {}
        for i in range(len(differences)-4):
            sequence = tuple(differences[i:i+4])
            if sequence not in first_sequence_prices:
                first_sequence_prices[sequence] = prices[i+4]
                all_sequences.add(sequence)
        all_first_sequence_prices.append(first_sequence_prices)
    best = 0
    best_sequence = None
    #print(len(all_sequences))
    for sequence in all_sequences:
        total = sum(first_sequence_prices.get(sequence, 0) for first_sequence_prices in all_first_sequence_prices)
        if total > best:
            best = total
            best_sequence = sequence
            if verbose:
                print(f'New best: {best} {sequence}')
    if verbose:
        print(best, best_sequence)
    return best

EXAMPLE2 = '''
1
2
3
2024
'''

assert solve2(EXAMPLE2) == 23

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
