EXAMPLE = '11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124'

def parse(s):
    def parse_range(s):
        return tuple(int(x) for x in s.split('-'))
    return [parse_range(x) for x in s.strip().split(',')]

def invalid(n):
    s = str(n)
    h = len(s) // 2
    return s[:h] == s[h:]

assert invalid(22)
assert invalid(2020)
assert not invalid(1)
assert not invalid(202)

def solve1(s):
    r = []
    for a, b in parse(s):
        for n in range(a, b+1):
            if invalid(n):
                r.append(n)
    return sum(r)

assert solve1(EXAMPLE) == 1227775554

def invalid2(n):
    s = str(n)
    length = len(s)
    for div in range(2, length+1):
        if length % div != 0:
            continue
        h = length // div
        first = s[0:h]
        if all(s[i:i+h] == first for i in range(h, length, h)):
            return True
    return False

assert invalid2(22)
assert invalid2(222)
assert invalid2(2121)
assert invalid2(212121)
assert not invalid2(21)
assert not invalid2(212)

def solve2(s):
    r = []
    for a, b in parse(s):
        for n in range(a, b+1):
            if invalid2(n):
                r.append(n)
    return sum(r)

assert solve2(EXAMPLE) == 4174379265

with open('input') as f:
    s = f.read()

print(solve1(s))
print(solve2(s))
