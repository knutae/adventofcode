import math

EXAMPLE = '''
Time:      7  15   30
Distance:  9  40  200
'''

def parse(data):
    times, distances = data.strip().split('\n')
    times = [int(x) for x in times.split()[1:]]
    distances = [int(x) for x in distances.split()[1:]]
    return times, distances

def solve1(data):
    times, distances = parse(data)
    r = []
    for time, distance in zip(times, distances):
        ways_to_solve = 0
        for button_time in range(1, time):
            travel_time = time - button_time
            dist = button_time * travel_time
            if dist > distance:
                ways_to_solve += 1
        r.append(ways_to_solve)
    return math.prod(r)

assert solve1(EXAMPLE) == 288

def solve2(data):
    times, distances = parse(data)
    time = int(''.join(map(str, times)))
    distance = int(''.join(map(str, distances)))
    ways_to_solve = 0
    for button_time in range(1, time):
        travel_time = time - button_time
        dist = button_time * travel_time
        if dist > distance:
            ways_to_solve += 1
    return ways_to_solve

assert solve2(EXAMPLE) == 71503

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
