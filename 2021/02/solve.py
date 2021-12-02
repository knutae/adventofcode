with open('input') as f:
    lines = f.read().strip().split('\n')

def solve1(lines):
    pos, depth = 0, 0
    for line in lines:
        command, n = line.split()
        n = int(n)
        if command == 'forward':
            pos += n
        elif command == 'down':
            depth += n
        elif command == 'up':
            depth -= n
        else:
            assert False
    #print(pos, depth)
    return pos * depth

def solve2(lines):
    pos, depth, aim = 0, 0, 0
    for line in lines:
        command, n = line.split()
        n = int(n)
        if command == 'forward':
            pos += n
            depth += n * aim
        elif command == 'down':
            aim += n
        elif command == 'up':
            aim -= n
        else:
            assert False
    #print(pos, depth)
    return pos * depth

assert solve1(['forward 5', 'down 5', 'forward 8', 'up 3', 'down 8', 'forward 2']) == 150
print(solve1(lines))
assert solve2(['forward 5', 'down 5', 'forward 8', 'up 3', 'down 8', 'forward 2']) == 900
print(solve2(lines))
