def solve1(positions):
    return min(sum(abs(p-m) for p in positions) for m in range(min(positions), max(positions)+1))

def move_cost(n):
    return n * (n+1) // 2

def solve2(positions):
    return min(sum(move_cost(abs(p-m)) for p in positions) for m in range(min(positions), max(positions)+1))

assert solve1([16,1,2,0,4,2,7,1,2,14]) == 37
assert solve2([16,1,2,0,4,2,7,1,2,14]) == 168

with open('input') as f:
    positions = [int(x) for x in f.read().strip().split(',')]

print(solve1(positions))
print(solve2(positions))
