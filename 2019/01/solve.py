import sys

def fuel(mass):
    return mass // 3 - 2

def total_fuel(mass):
    total = 0
    while True:
        extra = fuel(mass)
        if extra <= 0:
            break
        total += extra
        mass = extra
    return total

def solve1():
    input = [int(x) for x in sys.stdin]
    print(sum(fuel(x) for x in input))

def solve2():
    input = [int(x) for x in sys.stdin]
    print(sum(total_fuel(x) for x in input))

assert fuel(12) == 2
assert fuel(14) == 2
assert fuel(1969) == 654
assert fuel(100756) == 33583
assert total_fuel(14) == 2
assert total_fuel(1969) == 966
assert total_fuel(100756) == 50346

#solve1()
solve2()
