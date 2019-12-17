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

def solve_map(program):
    output = run_output(program)
    output = ''.join(chr(x) for x in output)
    print(output)
    tiles = defaultdict(str)
    y = 0
    x = 0
    width = 0
    for c in output:
        if c == '\n':
            y += 1
            width = max(width, x)
            x = 0
        else:
            tiles[(x,y)] = c
            x += 1
    height = y
    result = 0
    for x in range(width):
        for y in range(height):
            if (tiles[(x,y)] == '#' and
                tiles[(x-1,y)] == '#' and
                tiles[(x+1,y)] == '#' and
                tiles[(x,y-1)] == '#' and
                tiles[(x,y+1)] == '#'):
                print(f'aligned at {x},{y}')
                result += x*y
    print(result)
    return result

def indexes_of(path, sub, start):
    assert len(sub) > 0
    assert None not in sub
    return [i for i in range(start, len(path)-len(sub)+1) if path[i:i+len(sub)] == sub]

def generate_replacement_indexes(path, sub):
    indexes = indexes_of(path, sub, 0)
    for length in range(1, len(indexes)+1):
        for index_combo in itertools.combinations(indexes, length):
            if any(b - a < len(sub) for a, b in zip(index_combo, index_combo[1:])):
                # indexes too close to replace all
                continue
            yield index_combo

def generate_replacements(path, sub):
    replacement = [None] * len(sub)
    for index_combo in generate_replacement_indexes(path, sub):
        rpath = list(path)
        for index in index_combo:
            rpath[index:index+len(sub)] = replacement
        yield index_combo, rpath

def generate_substitution_candidates(path, min_length):
    if all(x is None for x in path):
        return
    start = min(i for i in range(len(path)) if path[i] is not None)
    path = path[start:]
    for length in range(min_length, len(path)+1):
        sub = path[:length]
        if sub[-1] == None:
            break
        yield sub

def main_function(index_dict):
    #print(index_dict)
    max_index = max(max(indexes) for indexes in index_dict.values())
    r = []
    for i in range(max_index+1):
        for key, indexes in index_dict.items():
            if i in indexes:
                r.append(key)
    return r

def generate_solution_candidates(path0, min_length=4):
    for sub0 in generate_substitution_candidates(path0, min_length):
        for index1, path1 in generate_replacements(path0, sub0):
            for sub1 in generate_substitution_candidates(path1, min_length):
                for index2, path2 in generate_replacements(path1, sub1):
                    for sub2 in generate_substitution_candidates(path2, min_length):
                        for index3, path3 in generate_replacements(path2, sub2):
                            if all(x is None for x in path3):
                                #yield (','.join(sub0), ','.join(sub1), ','.join(sub2))
                                a = ','.join(sub0)
                                b = ','.join(sub1)
                                c = ','.join(sub2)
                                main = ','.join(main_function({'A': index1, 'B': index2, 'C': index3}))
                                #print(' -- '.join([a,b,c,main]))
                                if all(len(x) <= 20 for x in (a,b,c,main)):
                                    yield main,a,b,c

def test2():
    assert indexes_of([1,1,3,1,1,1,4], [1,1], 0) == [0,3,4]
    assert indexes_of([1,1,3,1,1,1,4], [1,1], 2) == [3,4]
    assert indexes_of([1,2,3,1,1,1,4], [1,2], 0) == [0]
    #for x in generate_replacements([1,1,3,1,1,1,4], [1,1], [None,None]):
    #    print(x)
    assert [x[1] for x in generate_replacements([1,1,3,1,1,1,4], [1,1])] == [
        [None,None,3,1,1,1,4],
        [1,1,3,None,None,1,4],
        [1,1,3,1,None,None,4],
        [None,None,3,None,None,1,4],
        [None,None,3,1,None,None,4],
    ]
    assert list(generate_substitution_candidates([1,1,3], 1)) == [[1], [1,1], [1,1,3]]
    assert list(generate_substitution_candidates([1,1,None], 1)) == [[1], [1,1]]
    assert list(generate_substitution_candidates([None,1,3], 1)) == [[1], [1,3]]
    example = 'R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2'.split(',')
    candidates = list(generate_solution_candidates(example))
    #print(candidates)
    assert ('A,B,C,B,A,C', 'R,8,R,8', 'R,4,R,4,R,8', 'L,6,L,2') in candidates

test2()

def main():
    program = [int(x) for x in sys.stdin.read().strip().split(',')]
    solve_map(program)

def main2():
    path = 'L,12,L,6,L,8,R,6,L,8,L,8,R,4,R,6,R,6,L,12,L,6,L,8,R,6,L,8,L,8,R,4,R,6,R,6,L,12,R,6,L,8,L,12,R,6,L,8,L,8,L,8,R,4,R,6,R,6,L,12,L,6,L,8,R,6,L,8,L,8,R,4,R,6,R,6,L,12,R,6,L,8'.split(',')
    candidates = list(generate_solution_candidates(path))
    assert len(candidates) == 1
    print(candidates[0])
    program = [int(x) for x in sys.stdin.read().strip().split(',')]
    assert program[0] == 1
    program[0] = 2
    program_input = '\n'.join(candidates[0]) + '\nn\n'
    print(program_input)
    program_input = [ord(x) for x in program_input]
    print(program_input)
    output = run_output(program, program_input)
    #print(output)
    print(''.join(chr(x) for x in output[:-1]))
    print(output[-1])


#main()
main2()
