import sys
import itertools
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

def ascii_input(lines):
    return ArrayInput([ord(c) for c in '\n'.join(lines) + '\n'])

WALK_INSTRUCTIONS = [
    # jump if hole at A or C, and ground at D
    # safe to ignore B?
    'NOT C J', # hole at C
    'NOT A T', # hole at A
    'OR T J', # hole at A or C
    'AND D J', # ground at D
    'WALK',
]

RUN_INSTRUCTIONS = [
    # base logic: jump if hole at A, B or C, and ground at D
    # but also require ground at either E or H
    'NOT C J', # hole at C
    'NOT A T', # hole at A
    'OR T J', # hole at A or C
    'NOT B T', # hole at B
    'OR T J', # hole at A, B or C
    'AND D J', # ground at D

    'NOT E T', # hole at E
    'NOT T T', # ground at E
    'OR H T', # ground at E or H
    'AND T J',

    'RUN',
]

def main(program, instructions):
    output_line = []
    for c in run_yield(program, ascii_input(instructions)):
        if c > 128:
            print(f'Non-ascii: {c}')
        elif c == 10:
            print(''.join(output_line))
            output_line = []
        else:
            output_line.append(chr(c))

program = [int(x) for x in sys.stdin.read().strip().split(',')]
main(program, WALK_INSTRUCTIONS)
main(program, RUN_INSTRUCTIONS)
