from collections import defaultdict

EXAMPLE = '''
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
'''

def parse(s):
    lines = s.strip().split('\n')
    beam = lines[0].index('S')
    return beam, lines[1:]

def solve1(s):
    beam, lines = parse(s)
    beams = {beam}
    splits = 0
    for line in lines:
        new_beams = set()
        for beam in beams:
            if line[beam] == '^':
                new_beams.add(beam-1)
                new_beams.add(beam+1)
                splits += 1
            else:
                new_beams.add(beam)
        beams = new_beams
    return splits

assert solve1(EXAMPLE) == 21

def solve2(s):
    beam, lines = parse(s)
    timelines = {beam: 1}
    for line in lines:
        new_timelines = defaultdict(int)
        for beam, count in timelines.items():
            if line[beam] == '^':
                new_timelines[beam-1] += count
                new_timelines[beam+1] += count
            else:
                new_timelines[beam] += count
        timelines = new_timelines
    return sum(timelines.values())

assert solve2(EXAMPLE) == 40

with open('input') as f:
    s = f.read()

print(solve1(s))
print(solve2(s))
