import sys

def run(program):
    program = list(program)
    i = 0
    while True:
        opcode = program[i]
        if opcode == 99:
            break
        [a,b,c] = program[i+1:i+4]
        if opcode == 1:
            program[c] = program[a] + program[b]
        elif opcode == 2:
            program[c] = program[a] * program[b]
        else:
            assert False
        i += 4
    #print(program[0])
    return program

assert run([1,9,10,3,2,3,11,0,99,30,40,50]) == [3500,9,10,70,2,3,11,0,99,30,40,50]
assert run([1,0,0,0,99]) == [2,0,0,0,99]
assert run([2,3,0,3,99]) == [2,3,0,6,99]
assert run([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
assert run([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]

def solve(program, noun, verb):
    program = list(program)
    program[1] = noun
    program[2] = verb
    program = run(program)
    return program[0]

def solve1(program):
    res = solve(program, 12, 2)
    print(res)

def solve2(program, target):
    limit = 0
    while True:
        #print(limit)
        noun = limit
        for verb in range(0, limit+1):
            if solve(program, noun, verb) == target:
                print(noun, verb, 100*noun + verb)
                return 100*noun + verb
        limit += 1

program = [int(x) for x in sys.stdin.read().strip().split(',')]
assert solve(program, 12, 2) == 3654868
assert solve2(program, 3654868) == 1202
solve2(program, 19690720)
