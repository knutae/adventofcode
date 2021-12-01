with open('input') as f:
    depths = [int(x) for x in f.read().strip().split('\n')]

def solve1(depths):
    count = 0
    for a, b in zip(depths, depths[1:]):
        if b > a:
            count += 1
    return count

def solve2(depths):
    count = 0
    for a, b in zip(depths, depths[3:]):
        if b > a:
            count += 1
    return count

assert solve1([199, 200, 208, 210, 200, 207, 240, 269, 260, 263]) == 7
assert solve2([199, 200, 208, 210, 200, 207, 240, 269, 260, 263]) == 5

print(solve1(depths))
print(solve2(depths))
