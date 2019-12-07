import itertools
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
            # addition
            [a,b,c] = params(3)
            program[c] = getparam(a, 0) + getparam(b, 1)
        elif opcode == 2:
            # multiplication
            [a,b,c] = params(3)
            program[c] = getparam(a, 0) * getparam(b, 1)
        elif opcode == 3:
            # input
            [a] = params(1)
            program[a] = input[input_index]
            input_index += 1
        elif opcode == 4:
            # output
            [a] = params(1)
            r = getparam(a, 0)
            #print(r)
            output.append(r)
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
            program[c] = 1 if getparam(a, 0) < getparam(b, 1) else 0
        elif opcode == 8:
            # equals
            [a, b, c] = params(3)
            program[c] = 1 if getparam(a, 0) == getparam(b, 1) else 0
        else:
            assert False
    #print(program[0])
    return program

def run_output(program, input=[]):
    output = []
    run(program, input, output)
    return output

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

test()

def run_thrusters(program, phase_settings):
    signal = 0
    for p in phase_settings:
        output = run_output(program, [p, signal])
        assert len(output) == 1
        signal = output[0]
    return signal

def max_thruster_signal(program):
    return max(run_thrusters(program, phase_settings) for phase_settings in itertools.permutations(range(5)))

assert max_thruster_signal([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]) == 43210
assert max_thruster_signal([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]) == 54321
assert max_thruster_signal([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]) == 65210

program = [int(x) for x in sys.stdin.read().strip().split(',')]
print(max_thruster_signal(program))