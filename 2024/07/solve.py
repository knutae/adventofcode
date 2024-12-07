EXAMPLE = '''
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''

def parse_line(line):
    prefix, rest = line.split(': ')
    return int(prefix), [int(x) for x in rest.split()]

def parse(data):
    return [parse_line(line) for line in data.strip().split('\n')]

def can_combine(result, numbers):
    assert len(numbers) > 1
    if len(numbers) == 2:
        a, b = numbers
        return a + b == result or a * b == result
    last = numbers[-1]
    remaining = numbers[:-1]
    if can_combine(result - last, remaining):
        return True
    if result % last == 0 and can_combine(result // last, remaining):
        return True
    return False

def solve1(data):
    equations = parse(data)
    r = 0
    for result, numbers in equations:
        if can_combine(result, numbers):
            r += result
    return r

assert solve1(EXAMPLE) == 3749

with open('input') as f:
    data = f.read()

print(solve1(data))