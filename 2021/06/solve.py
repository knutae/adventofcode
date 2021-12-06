def solve(ages, num_days):
    counts_per_age = [0]*9
    for age in ages:
        counts_per_age[age] += 1
    for _ in range(num_days):
        respawns = counts_per_age[0]
        counts_per_age = counts_per_age[1:] + [respawns]
        counts_per_age[6] += respawns
    return sum(counts_per_age)

assert solve([3,4,3,1,2], 18) == 26
assert solve([3,4,3,1,2], 80) == 5934
assert solve([3,4,3,1,2], 256) == 26984457539

with open('input') as f:
    ages = [int(x) for x in f.read().split(',')]

print(solve(ages, 80))
print(solve(ages, 256))
