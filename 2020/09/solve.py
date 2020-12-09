def index_is_valid(all_numbers, index, length=25):
    assert index >= length and index < len(all_numbers)
    prev = all_numbers[index-length:index]
    n = all_numbers[index]
    for a in prev:
        b = n - a
        if a != b and b in prev:
            return True
    return False

def test_valid():
    numbers = list(range(1, 26))
    assert index_is_valid(numbers + [26], 25)
    assert index_is_valid(numbers + [49], 25)
    assert not index_is_valid(numbers + [100], 25)
    assert not index_is_valid(numbers + [50], 25)
    # make 20 the first number, add 45
    numbers[0], numbers[19] = numbers[19], numbers[0]
    assert numbers[0] == 20
    numbers.append(45)
    assert index_is_valid(numbers + [26], 26)
    assert not index_is_valid(numbers + [65], 26)
    assert index_is_valid(numbers + [64], 26)
    assert index_is_valid(numbers + [66], 26)

test_valid()

def solve1(numbers, length=25):
    for index in range(length, len(numbers)):
        if not index_is_valid(numbers, index, length):
            return numbers[index]
    assert False

assert solve1(
    [35,20,15,25,47,40,62,55,65,95,102,117,150,182,127,219,299,277,309,576],
    length=5) == 127

with open('input') as f:
    numbers = [int(line) for line in f.read().strip().split('\n')]

print(solve1(numbers))
