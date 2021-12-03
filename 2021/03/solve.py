EXAMPLE = '''
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
'''.strip().split('\n')

def solve1(lines):
    most_common = ''
    least_common = ''
    for i in range(len(lines[0])):
        bits = [line[i] for line in lines]
        zeroes = bits.count('0')
        ones = bits.count('1')
        assert zeroes != ones
        if zeroes > ones:
            most_common += '0'
            least_common += '1'
        else:
            most_common += '1'
            least_common += '0'
    gamma = int(most_common, 2)
    epsilon = int(least_common, 2)
    return gamma * epsilon

def filter_most_common(lines):
    for i in range(len(lines[0])):
        bits = [line[i] for line in lines]
        zeroes = bits.count('0')
        ones = bits.count('1')
        filter_bit = '1' if ones >= zeroes else '0'
        lines = [line for line in lines if line[i] == filter_bit]
        if len(lines) == 1:
            return lines[0]
    assert False

def filter_least_common(lines):
    for i in range(len(lines[0])):
        bits = [line[i] for line in lines]
        zeroes = bits.count('0')
        ones = bits.count('1')
        filter_bit = '0' if zeroes <= ones else '1'
        lines = [line for line in lines if line[i] == filter_bit]
        if len(lines) == 1:
            return lines[0]
    assert False

def solve2(lines):
    rating1 = int(filter_most_common(lines), 2)
    rating2 = int(filter_least_common(lines), 2)
    return rating1 * rating2

assert(solve1(EXAMPLE)) == 198
assert(solve2(EXAMPLE)) == 230

with open('input') as f:
    lines = f.read().strip().split('\n')

print(solve1(lines))
print(solve2(lines))
