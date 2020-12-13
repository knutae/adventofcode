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

with open('input') as f:
    timestamp, buses = parse1(f.read())

print(solve1(timestamp, buses))
