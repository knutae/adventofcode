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

def count_visible(asteroids, pos):
    px, py = pos
    count = 0
    for ax, ay in asteroids:
        if (ax,ay) == pos:
            continue
        visible = True
        dx = px - ax
        dy = py - ay
        for tx, ty in line_of_sight(dx, dy):
            tmp = ax + tx, ay + ty
            if tmp in asteroids:
                #print(f'{ax},{ay} blocked at {tmp}')
                visible = False
                break
            #else:
            #    print(f'{ax},{ay} NOT blocked at {tmp}')
        if visible:
            count += 1
    #print(count)
    return count

def best_location(asteroids):
    best = max(asteroids, key=lambda pos: count_visible(asteroids, pos))
    return best

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

test()

asteroids = parse(sys.stdin.read())
best = best_location(asteroids)
print(best)
print(count_visible(asteroids, best))
