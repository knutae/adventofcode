
def rfind(numbers, n, start):
    for i in range(start, -1, -1):
        if numbers[i] == n:
            return i
    return None

def solve1(numbers, length=2020):
    numbers = list(numbers)
    while len(numbers) < length:
        last_spoken = numbers[-1]
        last_index = rfind(numbers, last_spoken, len(numbers)-2)
        if last_index is None:
            numbers.append(0)
        else:
            numbers.append(len(numbers) - last_index - 1)
    #print(numbers)
    return numbers[-1]

assert solve1([0,3,6], 10) == 0
assert solve1([0,3,6]) == 436
assert solve1([1,3,2]) == 1
assert solve1([2,1,3]) == 10
assert solve1([1,2,3]) == 27
assert solve1([2,3,1]) == 78
assert solve1([3,2,1]) == 438
assert solve1([3,1,2]) == 1836

print(solve1([18,11,9,0,5,1]))
