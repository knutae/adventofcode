import sys
import itertools
from collections import deque

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

def run_step(program, input):
    ip = 0
    relative_base = 0
    param_modes = None

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

    def step():
        nonlocal param_modes, program, relative_base, ip
        instruction = program[ip]
        opcode = instruction % 100
        param_modes = instruction // 100
        ip += 1
        if opcode == 99:
            return 'quit'
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
            return r
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
        return None
    return step

def run_yield(program, input):
    step = run_step(program, input)
    while True:
        r = step()
        if r == 'quit':
            break
        if r is not None:
            yield r

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

class NetworkInput:
    def __init__(self, address):
        self.address = address
        self.local_queue = deque()
        self.local_queue.append(address)
        self.idle = False

    def next(self):
        if len(self.local_queue) == 0:
            self.idle = True
            return -1
        else:
            self.idle = False
            return self.local_queue.popleft()

    def extend(self, data):
        self.idle = False
        self.local_queue.extend(data)

class Computer:
    def __init__(self, program, address):
        self.input = NetworkInput(address)
        self.step_func = run_step(list(program), self.input)
        self.output_buffer = list()

    def step(self):
        r = self.step_func()
        assert r != 'quit'
        if r is not None:
            self.output_buffer.append(r)

def main():
    with open('input') as f:
        program = [int(x) for x in f.read().strip().split(',')]

    computers = [Computer(program, i) for i in range(50)]
    nat_buffer = None
    nat_last_delivered_y = None
    while True:
        for i, computer in enumerate(computers):
            assert len(computer.output_buffer) < 3
            computer.step()
            if len(computer.output_buffer) == 3:
                [address, x, y] = computer.output_buffer
                computer.output_buffer.clear()
                assert isinstance(address, int)
                assert isinstance(x, int)
                assert isinstance(y, int)
                print(f'Computer {i} output: address={address} x={x} y={y}')
                if address == 255:
                    #print(f'Result: {y}')
                    nat_buffer = [x, y]
                else:
                    assert address in range(50)
                    computers[address].input.extend([x, y])
        if all(c.input.idle for c in computers):
            if nat_buffer is None:
                #print('All idle, but no NAT buffer')
                continue
            assert nat_buffer is not None
            nat_y = nat_buffer[1]
            if nat_y == nat_last_delivered_y:
                print(f'Result: {nat_y}')
                return
            nat_last_delivered_y = nat_y
            computers[0].input.extend(nat_buffer)
            print(f'NAT delivered: {nat_buffer}')

main()
