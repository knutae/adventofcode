EXAMPLE = '''
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
'''

def parse_lock_or_key(section):
    lines = section.split('\n')
    if lines[0] == '#####':
        is_lock = True
        lines = lines[1:]
    else:
        assert lines[-1] == '#####'
        is_lock = False
        lines = lines[:-1]
    heights = [0 for _ in range(5)]
    for line in lines:
        for i, c in enumerate(line):
            if c == '#':
                heights[i] += 1
            else:
                assert c == '.'
    return is_lock, heights

def parse(data):
    sections = data.strip().split('\n\n')
    locks = []
    keys = []
    for s in sections:
        is_lock, x = parse_lock_or_key(s)
        if is_lock:
            locks.append(x)
        else:
            keys.append(x)
    return locks, keys

def overlaps(lock, key):
    return any(a + b > 5 for a, b in zip(lock, key))

def solve1(data):
    locks, keys = parse(data)
    return sum(1 for lock in locks for key in keys if not overlaps(lock, key))

assert solve1(EXAMPLE) == 3

with open('input') as f:
    data = f.read()

print(solve1(data))
