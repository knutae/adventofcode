import math
import sys

def parse(s):
    lines = s.strip().split('\n')
    return {(x,y)
        for y, line in enumerate(lines)
        for x, c in enumerate(line.strip())
        if c == '#'}

def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a

def line_of_sight(dx, dy):
    ax = abs(dx)
    ay = abs(dy)
    divisor = gcd(ax, ay)
    tx = dx // divisor
    ty = dy // divisor
    for i in range(1, divisor):
        yield i * tx, i * ty

def is_visible(asteroids, pos, a):
    assert pos != a
    px, py = pos
    ax, ay = a
    dx = px - ax
    dy = py - ay
    for tx, ty in line_of_sight(dx, dy):
        tmp = ax + tx, ay + ty
        if tmp in asteroids:
            #print(f'{ax},{ay} blocked at {tmp}')
            return False
        #else:
        #    print(f'{ax},{ay} NOT blocked at {tmp}')
    return True

def count_visible(asteroids, pos):
    count = 0
    for a in asteroids:
        if a == pos:
            continue
        if is_visible(asteroids, pos, a):
            count += 1
    #print(count)
    return count

def best_location(asteroids):
    best = max(asteroids, key=lambda pos: count_visible(asteroids, pos))
    return best

def to_angle(dx, dy):
    degrees = math.atan2(dx, -dy) * 180 / math.pi
    #print(degrees % 360.0)
    r = degrees % 360.0
    #if abs(360.0 - r) < 1e-10:
    #    # avoid rounding errors around 0.0
    #    return 0.0
    return r

def sorted_by_angle(asteroids, pos):
    px, py = pos
    return sorted(asteroids, key=lambda a: to_angle(a[0]-px, a[1]-py))

def vaporize(asteroids, pos):
    asteroids = set(asteroids)
    asteroids.remove(pos)
    while asteroids:
        to_remove = set()
        for a in sorted_by_angle(asteroids, pos):
            if is_visible(asteroids, pos, a):
                yield a
                to_remove.add(a)
        asteroids -= to_remove

def test():
    small_example = '''
.#..#
.....
#####
....#
...##
'''.strip()
    assert gcd(1, 0) == 1
    assert list(line_of_sight(1,1)) == []
    assert list(line_of_sight(1,2)) == []
    assert list(line_of_sight(0,3)) == [(0,1),(0,2)]
    assert list(line_of_sight(0,-3)) == [(0,-1),(0,-2)]
    assert list(line_of_sight(3,0)) == [(1,0),(2,0)]
    assert list(line_of_sight(-3,0)) == [(-1,0),(-2,0)]
    assert list(line_of_sight(3,3)) == [(1,1),(2,2)]
    assert list(line_of_sight(-3,3)) == [(-1,1),(-2,2)]
    assert list(line_of_sight(2,4)) == [(1,2)]
    assert list(line_of_sight(2,6)) == [(1,3)]
    assert list(line_of_sight(2,9)) == []
    assert list(line_of_sight(2,10)) == [(1,5)]
    assert list(line_of_sight(3,9)) == [(1,3),(2,6)]
    assert count_visible(parse(small_example), (3,4)) == 8
    assert best_location(parse(small_example)) == (3,4)
    assert abs(to_angle(0, -1)) < 1e-10
    assert abs(to_angle(1, 0) - 90.0) < 1e-10
    assert abs(to_angle(0, 1) - 180.0) < 1e-10
    assert abs(to_angle(-1, 0) - 270.0) < 1e-10
    assert abs(to_angle(1, 1) < 45.0) < 1e-10
    large_example = '''
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##'''
    asteroids = parse(large_example)
    assert best_location(asteroids) == (11,13)
    assert count_visible(asteroids, (11,13)) == 210
    vaporized = list(vaporize(asteroids, (11, 13)))
    assert len(vaporized) == 299
    assert vaporized[1-1] == (11,12)
    assert vaporized[2-1] == (12,1)
    assert vaporized[3-1] == (12,2)
    assert vaporized[10-1] == (12,8)
    assert vaporized[20-1] == (16,0)
    assert vaporized[50-1] == (16,9)
    assert vaporized[100-1] == (10,16)
    assert vaporized[199-1] == (9,6)
    assert vaporized[200-1] == (8,2)
    assert vaporized[201-1] == (10,9)
    assert vaporized[299-1] == (11,1)


test()

asteroids = parse(sys.stdin.read())
best = best_location(asteroids)
#print(best)
print(count_visible(asteroids, best))
vaporized = list(vaporize(asteroids, best))
print(vaporized[200-1])
x,y = vaporized[200-1]
print(x*100 + y)
