import sys

def solve1(numbers, verbose=False):
    for i, a in enumerate(numbers):
        for j, b in enumerate(numbers):
            if i != j and a + b == 2020:
                if verbose:
                    print(a, b)
                return a * b

def solve2(numbers, verbose=False):
    for i, a in enumerate(numbers):
        for j, b in enumerate(numbers):
            if i == j or a + b >= 2020:
                continue
            for k, c in enumerate(numbers):
                if a + b + c == 2020 and i != k and j != k:
                    if verbose:
                        print(a, b, c)
                    return a * b * c

assert solve1([1721, 979, 366, 299, 675, 1456]) == 514579
assert solve2([1721, 979, 366, 299, 675, 1456]) == 241861950

numbers = [int(x.strip()) for x in sys.stdin.readlines() if x.strip()]
#print(solve1(numbers, True))
print(solve2(numbers, True))
