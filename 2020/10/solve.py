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

with open('input') as f:
    numbers = [int(x) for x in f.read().strip().split('\n')]
print(solve1(numbers))
