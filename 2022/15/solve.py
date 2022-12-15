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

def solve1(input, row):
    x_positions = set()
    x_beacons = set()
    for sensor, beacon in parse(input):
        r = sensor_range_at_row(sensor, beacon, row)
        for x in r:
            x_positions.add(x)
        if beacon[1] == row:
            x_beacons.add(beacon[0])
    return len(x_positions.difference(x_beacons))

assert sensor_range_at_row((8,7), (2,10), -3) == range(0)
assert sensor_range_at_row((8,7), (2,10), -2) == range(8, 9)
assert sensor_range_at_row((8,7), (2,10), 7) == range(-1, 18)
assert sensor_range_at_row((8,7), (2,10), 10) == range(2, 15)
assert sensor_range_at_row((8,7), (2,10), 16) == range(8, 9)
assert sensor_range_at_row((8,7), (2,10), 17) == range(0)

assert solve1(EXAMPLE, 10) == 26

with open('input') as f:
    input = f.read()

print(solve1(input, 2000000))
