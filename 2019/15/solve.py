import sys
import random
from collections import defaultdict

class Input:
    def next(self):
        pass

class ArrayInput(Input):
    def __init__(self, array):
        self.array = array
        self.index = 0

    def next(self):
        r = self.array[self.index]
        self.index += 1
        return r

class ManualInput(Input):
    def __init__(self, value):
        self.value = value

    def next(self):
        #print(f"input: {self.value}")
        return self.value

def array_input(array):
    input_index = 0
    try:
        while True:
            yield array[input_index]
            input_index += 1
    except IndexError:
        raise StopIteration()

def run_yield(program, input):
    ip = 0
    relative_base = 0

    def params(n):
        nonlocal ip, program
        p = program[ip:ip+n]
        ip += n
        return p
    
    def extend_memory_if_needed(index):
        nonlocal program
        while index >= len(program):
            program.append(0)


    def getparam(value, i):
        nonlocal param_modes, program, relative_base
        div = 10**i
        mode = (param_modes // div) % 10
        if mode == 0:
            # position mode
            extend_memory_if_needed(value)
            return program[value]
        elif mode == 1:
            # immediate mode
            return value
        elif mode == 2:
            # relative mode
            extend_memory_if_needed(value + relative_base)
            return program[value + relative_base]
        else:
            assert False
    
    def setindex(value, i):
        nonlocal param_modes, program, relative_base
        div = 10**i
        mode = (param_modes // div) % 10
        if mode == 0:
            # position mode
            extend_memory_if_needed(value)
            return value
        elif mode == 2:
            # relative mode
            extend_memory_if_needed(value + relative_base)
            return value + relative_base
        else:
            assert False

    while True:
        instruction = program[ip]
        opcode = instruction % 100
        param_modes = instruction // 100
        ip += 1
        if opcode == 99:
            break
        if opcode == 1:
            # addition
            [a,b,c] = params(3)
            program[setindex(c, 2)] = getparam(a, 0) + getparam(b, 1)
        elif opcode == 2:
            # multiplication
            [a,b,c] = params(3)
            program[setindex(c, 2)] = getparam(a, 0) * getparam(b, 1)
        elif opcode == 3:
            # input
            [a] = params(1)
            program[setindex(a, 0)] = input.next()
        elif opcode == 4:
            # output
            [a] = params(1)
            r = getparam(a, 0)
            yield r
            #print(r)
        elif opcode == 5:
            # jump-if-true
            [a, b] = params(2)
            if getparam(a, 0) != 0:
                ip = getparam(b, 1)
        elif opcode == 6:
            # jump-if-false
            [a, b] = params(2)
            if getparam(a, 0) == 0:
                ip = getparam(b, 1)
        elif opcode == 7:
            # less than
            [a, b, c] = params(3)
            program[setindex(c, 2)] = 1 if getparam(a, 0) < getparam(b, 1) else 0
        elif opcode == 8:
            # equals
            [a, b, c] = params(3)
            program[setindex(c, 2)] = 1 if getparam(a, 0) == getparam(b, 1) else 0
        elif opcode == 9:
            [a] = params(1)
            relative_base += getparam(a, 0)
        else:
            assert False

def run_output(program, input=[]):
    return list(run_yield(list(program), ArrayInput(input)))

def run(program, input=[]):
    program = list(program)
    list(run_yield(program, ArrayInput(input)))
    return program

def test():
    assert run([1,9,10,3,2,3,11,0,99,30,40,50]) == [3500,9,10,70,2,3,11,0,99,30,40,50]
    assert run([1,0,0,0,99]) == [2,0,0,0,99]
    assert run([2,3,0,3,99]) == [2,3,0,6,99]
    assert run([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
    assert run([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]
    assert run_output([3,0,4,0,99], [42]) == [42]
    assert run_output([104,42,99], []) == [42]
    assert run([1002,4,3,4,33]) == [1002,4,3,4,99]
    assert run_output([3,9,8,9,10,9,4,9,99,-1,8], [7]) == [0]
    assert run_output([3,9,8,9,10,9,4,9,99,-1,8], [8]) == [1]
    assert run_output([3,9,8,9,10,9,4,9,99,-1,8], [9]) == [0]
    assert run_output([3,9,7,9,10,9,4,9,99,-1,8], [7]) == [1]
    assert run_output([3,9,7,9,10,9,4,9,99,-1,8], [8]) == [0]
    assert run_output([3,9,7,9,10,9,4,9,99,-1,8], [9]) == [0]
    assert run_output([3,3,1108,-1,8,3,4,3,99], [7]) == [0]
    assert run_output([3,3,1108,-1,8,3,4,3,99], [8]) == [1]
    assert run_output([3,3,1108,-1,8,3,4,3,99], [9]) == [0]
    assert run_output([3,3,1107,-1,8,3,4,3,99], [7]) == [1]
    assert run_output([3,3,1107,-1,8,3,4,3,99], [8]) == [0]
    assert run_output([3,3,1107,-1,8,3,4,3,99], [9]) == [0]
    assert run_output([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [0]) == [0]
    assert run_output([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [-1]) == [1]
    assert run_output([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [0]) == [0]
    assert run_output([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [-42]) == [1]
    example = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
    assert run_output(example, [7]) == [999]
    assert run_output(example, [8]) == [1000]
    assert run_output(example, [9]) == [1001]
    relative_example = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    assert run_output(relative_example) == relative_example
    assert run_output([1102,34915192,34915192,7,4,7,99,0]) == [1219070632396864]
    assert run_output([104,1125899906842624,99]) == [1125899906842624]

test()

def draw_map(tiles, robot):
    xmin = min(tiles, key=lambda p:p[0])[0]
    xmax = max(tiles, key=lambda p:p[0])[0]
    ymin = min(tiles, key=lambda p:p[1])[1]
    ymax = max(tiles, key=lambda p:p[1])[1]
    for y in range(ymin, ymax+1):
        line = ['D' if robot == (x,y) else 'A' if (x,y) == (0,0) else tiles[(x,y)] for x in range(xmin,xmax+1)]
        print(''.join(line))

def target_pos(robot, direction):
    x, y = robot
    if direction == 1:
        # north
        return x, y-1
    elif direction == 2:
        # south
        return x, y+1
    elif direction == 3:
        # west
        return x-1, y
    elif direction == 4:
        # east
        return x+1, y
    assert False

def translate_direction(s):
    directions = {
        'w': 1,
        's': 2,
        'a': 3,
        'd': 4
    }
    return directions[s]

def random_direction():
    return random.choice([1,2,3,4])

def choose_direction(tiles, robot):
    unexplored = []
    backtrack = []
    for d in [1,2,3,4]:
        target = target_pos(robot, d)
        if target not in tiles:
            unexplored.append(d)
        elif tiles[target] != '#':
            backtrack.append(d)
    if unexplored:
        return random.choice(unexplored)
    assert backtrack
    return random.choice(backtrack)

def explore(program):
    manual_input = ManualInput(0)
    tiles = defaultdict(lambda:' ')
    robot = (0,0)
    tiles[robot] = '.'
    generator = run_yield(program, manual_input)
    #while True:
    for _ in range(100000):
        #draw_map(tiles, robot)
        #direction = int(input())
        #direction = translate_direction(input())
        #direction = random_direction()
        direction = choose_direction(tiles, robot)
        target = target_pos(robot, direction)
        manual_input.value = direction
        result = next(generator)
        if result == 0:
            # wall
            tiles[target] = '#'
        elif result == 1:
            # move
            tiles[target] = '.'
            robot = target
        elif result == 2:
            print(f'Found oxygen at {target}!')
            tiles[target] = 'o'
            robot = target
        else:
            assert False
    draw_map(tiles, robot)

def parse_map(s):
    lines = s.rstrip().split('\n')
    walls = set()
    start = None
    dest = None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            pos = (x,y)
            if c == '#':
                walls.add(pos)
            elif c == 'A':
                start = pos
            elif c == 'o':
                dest = pos
            else:
                assert c in '. D'
    assert start is not None
    assert dest is not None
    return frozenset(walls), start, dest

def shortest_path(walls, start, dest):
    visited = set()
    candidates = {start}
    iterations = 0
    while dest not in candidates:
        iterations += 1
        visited |= candidates
        new_candidates = set()
        for pos in candidates:
            for direction in [1,2,3,4]:
                target = target_pos(pos, direction)
                if target not in visited and target not in walls:
                    new_candidates.add(target)
        candidates = new_candidates
    return iterations

def debug_print(walls, visited):
    for y in range(42):
        print(''.join('O' if (x,y) in visited else '#' if (x,y) in walls else ' ' for x in range(42)))

def fill_map(walls, start):
    visited = set()
    candidates = {start}
    iterations = 0
    while candidates:
        iterations += 1
        visited |= candidates
        new_candidates = set()
        for pos in candidates:
            for direction in [1,2,3,4]:
                target = target_pos(pos, direction)
                if target not in visited and target not in walls:
                    new_candidates.add(target)
        candidates = new_candidates
        #debug_print(walls, visited)
    return iterations - 1

def main_explore():
    with open('input') as f:
        program = [int(x) for x in f.read().strip().split(',')]
    explore(program)
    #solve(program)

def main_solve():
    with open('map') as f:
        walls, start, dest = parse_map(f.read())
    print(shortest_path(walls, start, dest))
    print(fill_map(walls, dest))

#main_explore()
main_solve()
