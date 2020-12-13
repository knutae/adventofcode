EXAMPLE = '''
939
7,13,x,x,59,x,31,19
'''

def parse1(input):
    lines = input.strip().split('\n')
    assert len(lines) == 2
    timestamp = int(lines[0])
    buses = [int(n) for n in lines[1].split(',') if n != 'x']
    return timestamp, buses

assert parse1(EXAMPLE) == (939, [7,13,59,31,19])

def minutes_until_departure(timestamp, bus):
    remainder = timestamp % bus
    if remainder == 0:
        return 0
    else:
        return bus - remainder

def solve1(timestamp, buses):
    bus = min(buses, key=lambda bus: minutes_until_departure(timestamp, bus))
    return bus * minutes_until_departure(timestamp, bus)

assert solve1(*parse1(EXAMPLE)) == 295

def parse2(input):
    lines = input.strip().split('\n')
    assert len(lines) in (1,2)
    buses = {int(n): offset for offset, n in enumerate(lines[-1].split(',')) if n != 'x'}
    for bus in buses:
        if buses[bus] >= bus:
            new_index = buses[bus] % bus
            #print(f'Modifying bus index for {bus}: {buses[bus]} -> {new_index}')
            buses[bus] = new_index
        assert buses[bus] < bus
    return buses

assert parse2(EXAMPLE) == {7:0, 13:1, 59:4, 31:6, 19:7}

def solve2(buses):
    buses = dict(buses)
    timestamp = 0
    timeskip = 1
    total_iterations = 0
    while len(buses) > 0:
        bus = min(buses)
        while minutes_until_departure(timestamp, bus) != buses[bus]:
            timestamp += timeskip
            total_iterations += 1
        #print(f'Matched bus {bus} at timestamp {timestamp}, modifying timeskip {timeskip} -> {timeskip * bus}, total iterations {total_iterations}')
        timeskip *= bus
        del buses[bus]
    return timestamp

assert solve2(parse2(EXAMPLE)) == 1068781
assert solve2(parse2('17,x,13,19')) == 3417
assert solve2(parse2('67,7,59,61')) == 754018
assert solve2(parse2('67,x,7,59,61')) == 779210
assert solve2(parse2('1789,37,47,1889')) == 1202161486

with open('input') as f:
    input = f.read()

timestamp, buses = parse1(input)
print(solve1(timestamp, buses))

buses = parse2(input)
print(solve2(buses))
