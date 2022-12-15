EXAMPLE = '''
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''

def strip_prefix(s, prefix):
    assert s.startswith(prefix)
    return s[len(prefix):]

def parse_point(p):
    [x, y] = p.split(', ')
    return int(strip_prefix(x, 'x=')), int(strip_prefix(y, 'y='))

def parse_line(line):
    [a, b] = line.split(': closest beacon is at ')
    a = strip_prefix(a, 'Sensor at ')
    return parse_point(a), parse_point(b)

def parse(input):
    return [parse_line(line) for line in input.strip().split('\n')]

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def sensor_range_at_row(sensor, beacon, row):
    sensor_size = manhattan_distance(sensor, beacon)
    y_dist = abs(sensor[1] - row)
    x_dist = sensor_size - y_dist
    if x_dist < 0:
        return range(0)
    return range(sensor[0] - x_dist, sensor[0] + x_dist + 1)

def join_ranges(a, b):
    assert a.start <= b.start
    if a.stop >= b.start:
        return range(a.start, max(a.stop, b.stop))
    return None

def simplify_ranges(ranges):
    ranges.sort(key=lambda r:r.start)
    while len(ranges) > 1:
        for i in range(len(ranges) - 1):
            joined = join_ranges(ranges[i], ranges[i+1])
            if joined:
                ranges = ranges[0:i] + [joined] + ranges[i+2:]
                break
        else:
            break
    return ranges

def split_ranges(ranges, n):
    new_ranges = []
    for r in ranges:
        if n in r:
            if len(r) == 1:
                continue
            if n > r.start:
                new_ranges.append(range(r.start, n))
            if n < r.stop - 1:
                new_ranges.append(range(n+1, r.stop))
        else:
            new_ranges.append(r)
    return new_ranges

def crop_ranges(ranges, low, high):
    new_ranges = []
    for r in ranges:
        if r.stop <= low or r.start > high:
            continue
        new_ranges.append(range(max(low, r.start), min(high, r.stop)))
    return new_ranges

def solve1(input, row):
    x_ranges = []
    x_beacons = set()
    for sensor, beacon in parse(input):
        r = sensor_range_at_row(sensor, beacon, row)
        x_ranges.append(r)
        x_ranges = simplify_ranges(x_ranges)
        if beacon[1] == row:
            x_beacons.add(beacon[0])
    for x in x_beacons:
        x_ranges = split_ranges(x_ranges, x)
    return sum(len(r) for r in x_ranges)

def solve2(input, low, high):
    candidates = []
    parsed = parse(input)
    for row in range(low, high+1):
        x_ranges = []
        for sensor, beacon in parsed:
            r = sensor_range_at_row(sensor, beacon, row)
            x_ranges.append(r)
        x_ranges = simplify_ranges(x_ranges)
        x_ranges = crop_ranges(x_ranges, low, high+1)
        if x_ranges != [range(low, high+1)]:
            #print(row, x_ranges)
            assert len(x_ranges) == 2
            assert x_ranges[0].stop + 1 == x_ranges[1].start
            candidates.append((x_ranges[0].stop, row))
    assert len(candidates) == 1
    x, y = candidates[0]
    return x * 4000000 + y

assert sensor_range_at_row((8,7), (2,10), -3) == range(0)
assert sensor_range_at_row((8,7), (2,10), -2) == range(8, 9)
assert sensor_range_at_row((8,7), (2,10), 7) == range(-1, 18)
assert sensor_range_at_row((8,7), (2,10), 10) == range(2, 15)
assert sensor_range_at_row((8,7), (2,10), 16) == range(8, 9)
assert sensor_range_at_row((8,7), (2,10), 17) == range(0)
assert simplify_ranges([]) == []
assert simplify_ranges([range(1,3)]) == [range(1,3)]
assert simplify_ranges([range(1,3), range(4,10)]) == [range(1,3), range(4,10)]
assert simplify_ranges([range(1,3), range(3,10)]) == [range(1,10)]
assert simplify_ranges([range(3,10), range(1,3)]) == [range(1,10)]
assert crop_ranges([range(1,5), range(10, 20), range(25, 40), range(50, 60)], 15, 30) == [range(15, 20), range(25, 30)]

assert solve1(EXAMPLE, 10) == 26
assert solve2(EXAMPLE, 0, 20) == 56000011

with open('input') as f:
    input = f.read()

print(solve1(input, 2000000))
print(solve2(input, 0, 4000000))
