EXAMPLE1 = '''
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
'''

EXAMPLE2 = '''
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
'''

def parse_line(line):
    return eval(line)

def parse(data):
    return [parse_line(line) for line in data.strip().split('\n')]

def recursive_len(sn, level=0, max_level=4):
    assert level <= max_level
    if level == max_level or isinstance(sn, int):
        return 1
    left, right = sn
    return recursive_len(left, level+1, max_level) + recursive_len(right, level+1, max_level)

assert recursive_len([1,2]) == 2
assert recursive_len([[[[0,9],2],3],4]) == 5
assert recursive_len([[[[[9,8],1],2],3],4]) == 5

def recursive_get(sn, index, level=0, max_level=4):
    if index == 0 and (level == max_level or isinstance(sn, int)):
        return sn
    left, right = sn
    left_len = recursive_len(left, level+1, max_level)
    if index < left_len:
        return recursive_get(left, index, level+1, max_level)
    else:
        return recursive_get(right, index - left_len, level+1, max_level)

assert recursive_get([1,2], 0) == 1
assert recursive_get([1,2], 1) == 2
assert recursive_get([[[[0,9],2],3],4], 0) == 0
assert recursive_get([[[[0,9],2],3],4], 1) == 9
assert recursive_get([[[[0,9],2],3],4], 2) == 2
assert recursive_get([[[[0,9],2],3],4], 3) == 3
assert recursive_get([[[[0,9],2],3],4], 4) == 4
assert recursive_get([[[[[9,8],1],2],3],4], 0) == [9,8]
assert recursive_get([[[[[9,8],1],2],3],4], 1) == 1

def recursive_set(sn, index, value, level=0, max_level=4):
    if index == 0 and (level == max_level or isinstance(sn, int)):
        return value
    left, right = sn
    left_len = recursive_len(left, level+1, max_level)
    if index < left_len:
        return [recursive_set(left, index, value, level+1, max_level), right]
    else:
        return [left, recursive_set(right, index - left_len, value, level+1, max_level)]

assert recursive_set([1,2],0,[3,4]) == [[3,4],2]
assert recursive_set([1,2],1,[3,4]) == [1,[3,4]]
assert recursive_set([[[[[9,8],1],2],3],4], 0, 0) == [[[[0,1],2],3],4]

def explode(sn):
    length = recursive_len(sn)
    for index in range(length):
        candidate = recursive_get(sn, index)
        if isinstance(candidate, int):
            continue
        left, right = recursive_get(sn, index)
        result = recursive_set(sn, index, 0)
        if index > 0:
            result = recursive_set(result, index - 1, left + recursive_get(result, index - 1))
        # need to support incrementing numbers with level 4, so pass max_level=5 below
        if index < recursive_len(result, max_level=5) - 1:
            result = recursive_set(result, index + 1, right + recursive_get(result, index + 1, max_level=5), max_level=5)
        return result
    return None

assert explode([[[[[9,8],1],2],3],4]) == [[[[0,9],2],3],4]
assert explode([7,[6,[5,[4,[3,2]]]]]) == [7,[6,[5,[7,0]]]]
assert explode([[6,[5,[4,[3,2]]]],1]) == [[6,[5,[7,0]]],3]
assert explode([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
assert explode([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[7,0]]]]

def split(sn):
    length = recursive_len(sn)
    for index in range(length):
        candidate = recursive_get(sn, index)
        if isinstance(candidate, list) or candidate < 10:
            continue
        left = candidate // 2
        right = left + candidate % 2
        return recursive_set(sn, index, [left, right])
    return None

assert split([[[[0,7],4],[15,[0,13]]],[1,1]]) == [[[[0,7],4],[[7,8],[0,13]]],[1,1]]

def reduce(sn):
    current = sn
    while True:
        candidate = explode(current)
        if candidate is None:
            candidate = split(current)
        if candidate is None:
            return current
        current = candidate

def add(left, right):
    return reduce([left, right])

assert add([[[[4,3],4],4],[7,[[8,4],9]]], [1,1]) == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

def sum_list(sn_list, verbose=False):
    result = sn_list[0]
    for sn in sn_list[1:]:
        if verbose:
            print(f"\n  {result}")
        result = add(result, sn)
        if verbose:
            print(f"+ {sn}\n= {result}")
    return result

assert sum_list([[1,1], [2,2], [3,3], [4,4]]) == [[[[1,1],[2,2]],[3,3]],[4,4]]
assert sum_list([[1,1], [2,2], [3,3], [4,4], [5,5]]) == [[[[3,0],[5,3]],[4,4]],[5,5]]
assert sum_list([[1,1], [2,2], [3,3], [4,4], [5,5], [6,6]]) == [[[[5,0],[7,4]],[5,5]],[6,6]]
assert sum_list(parse(EXAMPLE1)) == [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]
assert sum_list(parse(EXAMPLE2)) == [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]

def magnitude(sn):
    if isinstance(sn, int):
        return sn
    left, right = sn
    return 3*magnitude(left) + 2*magnitude(right)

assert magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]) == 3488

def solve1(data):
    return magnitude(sum_list(parse(data)))

assert solve1(EXAMPLE2) == 4140

def solve2(data):
    sn_list = parse(data)
    result = 0
    for a in sn_list:
        for b in sn_list:
            if a != b:
                result = max(result, magnitude(add(a, b)))
    return result

assert solve2(EXAMPLE2) == 3993

with open('input') as f:
    puzzle_input = f.read()

print(solve1(puzzle_input))
print(solve2(puzzle_input))
