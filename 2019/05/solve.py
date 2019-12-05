import sys

def run(program, input=[], output=[]):
    program = list(program)
    ip = 0
    input_index = 0

    def params(n):
        nonlocal ip, program
        p = program[ip:ip+n]
        ip += n
        return p

    def getparam(value, i):
        nonlocal param_modes, program
        div = 10**i
        mode = (param_modes // div) % 10
        if mode == 0:
            # parameter mode
            return program[value]
        elif mode == 1:
            # immediate mode
            return value
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
            [a,b,c] = params(3)
            program[c] = getparam(a, 0) + getparam(b, 1)
        elif opcode == 2:
            [a,b,c] = params(3)
            program[c] = getparam(a, 0) * getparam(b, 1)
        elif opcode == 3:
            [a] = params(1)
            program[a] = input[input_index]
            input_index += 1
        elif opcode == 4:
            [a] = params(1)
            r = getparam(a, 0)
            #print(r)
            output.append(r)
        else:
            assert False
    #print(program[0])
    return program

def run_output(program, input=[]):
    output = []
    run(program, input, output)
    return output

assert run([1,9,10,3,2,3,11,0,99,30,40,50]) == [3500,9,10,70,2,3,11,0,99,30,40,50]
assert run([1,0,0,0,99]) == [2,0,0,0,99]
assert run([2,3,0,3,99]) == [2,3,0,6,99]
assert run([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
assert run([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]
assert run_output([3,0,4,0,99], [42]) == [42]
assert run_output([104,42,99], []) == [42]
assert run([1002,4,3,4,33]) == [1002,4,3,4,99]

def solve(program, input=[1]):
    r = run_output(program, input)
    print(r)
    return r

program = [int(x) for x in sys.stdin.read().strip().split(',')]
solve(program)
