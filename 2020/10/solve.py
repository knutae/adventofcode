import itertools

EXAMPLE1 = [16,10,15,5,1,11,7,19,6,12,4]
EXAMPLE2 = [28,33,18,42,31,14,46,20,48,47,24,23,49,45,19,38,39,11,1,32,25,35,8,17,7,9,4,2,34,10,3]

def solve1(numbers):
    prev = -1000
    diffs_1 = 0
    diffs_3 = 0
    #print(list(sorted(numbers)))
    for n in sorted([0] + numbers + [max(numbers) + 3]):
        if n - prev == 1:
            diffs_1 += 1
        elif n - prev == 3:
            diffs_3 += 1
        prev = n
    #print(diffs_1, diffs_3)
    return diffs_1 * diffs_3

assert solve1(EXAMPLE1) == 35
assert solve1(EXAMPLE2) == 220

def is_valid_range(numbers):
    for i in range(1, len(numbers)):
        diff = numbers[i] - numbers[i-1]
        assert diff > 0
        if diff > 3:
            return False
    return True

def generate_valid_combinations(numbers):
    "Brute force implementation. The first and last number are always included."
    assert len(numbers) > 0
    if len(numbers) == 1:
        yield numbers
    first = numbers[0]
    last = numbers[-1]
    rest = numbers[1:-1]
    # length = 0 is included, which is important!
    for length in range(len(rest)+1):
        for combo in itertools.combinations(rest, length):
            full_combo = (first, *combo, last)
            if is_valid_range(full_combo):
                yield full_combo

def split(numbers):
    sublist = [numbers[0]]
    for n in numbers[1:]:
        diff = n - sublist[-1]
        sublist.append(n)
        assert diff > 0 and diff <= 3
        if diff == 3:
            # split
            yield sublist
            sublist = [n]
    assert len(sublist) == 1 # no need to yield this

def solve2(numbers):
    all_numbers = [0] + list(sorted(numbers)) + [max(numbers) + 3]
    result = 1
    for sublist in split(all_numbers):
        #print(sublist)
        count = sum(1 for x in generate_valid_combinations(sublist))
        #print(count)
        result *= count
    return result

assert solve2(EXAMPLE1) == 8
assert solve2(EXAMPLE2) == 19208

with open('input') as f:
    numbers = [int(x) for x in f.read().strip().split('\n')]
print(solve1(numbers))
print(solve2(numbers))
