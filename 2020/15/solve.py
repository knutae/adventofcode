def solve1(numbers, length=2020):
    indexes = {n: index for index, n in enumerate(numbers[:-1])}
    last_spoken = numbers[-1]
    for i in range(len(numbers), length):
        if last_spoken in indexes:
            next_spoken = i - indexes[last_spoken] - 1
        else:
            next_spoken = 0
        indexes[last_spoken] = i - 1
        last_spoken = next_spoken
    return last_spoken

def solve2(numbers):
    print(numbers)
    return solve1(numbers, 30000000)

assert solve1([0,3,6], 10) == 0
assert solve1([0,3,6]) == 436
assert solve1([1,3,2]) == 1
assert solve1([2,1,3]) == 10
assert solve1([1,2,3]) == 27
assert solve1([2,3,1]) == 78
assert solve1([3,2,1]) == 438
assert solve1([3,1,2]) == 1836

print(solve1([18,11,9,0,5,1]))

# slow, but not too bad:
assert solve2([0,3,6]) == 175594
assert solve2([1,3,2]) == 2578
assert solve2([2,1,3]) == 3544142
assert solve2([1,2,3]) == 261214
assert solve2([2,3,1]) == 6895259
assert solve2([3,2,1]) == 18
assert solve2([3,1,2]) == 362

print(solve2([18,11,9,0,5,1]))
