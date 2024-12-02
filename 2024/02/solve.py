EXAMPLE = '''
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
'''

def parse(data):
    lines = data.strip().split('\n')
    return [
        [int(x) for x in line.split()]
        for line in lines
    ]

def is_safe(report):
    zipped = list(zip(report, report[1:]))
    increasing = all(a < b for a, b in zipped)
    decreasing = all(a > b for a, b in zipped)
    if not (increasing or decreasing):
        return False
    if any(abs(a-b) > 3 for a, b in zipped):
        return False
    return True

def solve1(data):
    reports = parse(data)
    r = sum(is_safe(r) for r in reports)
    return r

def is_safe_with_dampening(report):
    if is_safe(report):
        return True
    for i in range(len(report)):
        dampened = report[:i] + report[i+1:]
        if is_safe(dampened):
            return True
    return False

def solve2(data):
    reports = parse(data)
    r = sum(is_safe_with_dampening(r) for r in reports)
    return r

assert solve1(EXAMPLE) == 2
assert solve2(EXAMPLE) == 4

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
