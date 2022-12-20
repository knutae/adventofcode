EXAMPLE = '''
1
2
-3
3
-2
0
4
'''

def parse(input):
    return [int(x) for x in input.strip().split('\n')]

def move(current_numbers, original_index, n):
    current_index = current_numbers.index((original_index, n))
    del current_numbers[current_index]
    new_index = (current_index + n) % len(current_numbers)
    current_numbers.insert(new_index, (original_index, n))

def solve1(input):
    numbers = parse(input)
    current_numbers = list(enumerate(numbers))
    for i, n in enumerate(numbers):
        move(current_numbers, i, n)
    zero_index = [i for i, num in enumerate(current_numbers) if num[1] == 0]
    assert len(zero_index) == 1
    zero_index = zero_index[0]
    results = [current_numbers[(zero_index + x) % len(current_numbers)][1] for x in (1000, 2000, 3000)]
    #print(results)
    return sum(results)

def solve2(input):
    numbers = parse(input)
    numbers = [n*811589153 for n in numbers]
    current_numbers = list(enumerate(numbers))
    for _ in range(10):
        for i, n in enumerate(numbers):
            move(current_numbers, i, n)
    zero_index = [i for i, num in enumerate(current_numbers) if num[1] == 0]
    assert len(zero_index) == 1
    zero_index = zero_index[0]
    results = [current_numbers[(zero_index + x) % len(current_numbers)][1] for x in (1000, 2000, 3000)]
    #print(results)
    return sum(results)

assert solve1(EXAMPLE) == 3
assert solve2(EXAMPLE) == 1623178306

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
