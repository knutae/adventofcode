EXAMPLE_PROGRAM = '''
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
'''

def parse_instruction(line):
    [op, n] = line.split(' ')
    assert op in ('nop', 'acc', 'jmp')
    return op, int(n)

def parse(input):
    return [parse_instruction(line) for line in input.strip().split('\n')]

class Program:
    def __init__(self, instructions):
        self.instructions = instructions
        self.instruction_pointer = 0
        self.accumulator = 0

    def step(self):
        op, n = self.instructions[self.instruction_pointer]
        if op == 'nop':
            self.instruction_pointer += 1
        elif op == 'acc':
            self.accumulator += n
            self.instruction_pointer += 1
        elif op == 'jmp':
            self.instruction_pointer += n
        else:
            assert False

    def terminated(self):
        return self.instruction_pointer == len(self.instructions)

def solve1(program):
    visited = set()
    while program.instruction_pointer not in visited:
        visited.add(program.instruction_pointer)
        program.step()
    return program.accumulator

assert solve1(Program(parse(EXAMPLE_PROGRAM))) == 5

def terminates(program):
    visited = set()
    while program.instruction_pointer not in visited:
        visited.add(program.instruction_pointer)
        program.step()
        if program.terminated():
            return True
    return False

def modify_instruction(program, index):
    op, n = program.instructions[index]
    if op == 'jmp':
        mod = 'nop'
    elif op == 'nop':
        mod = 'jmp'
    else:
        return None
    instructions = list(program.instructions)
    instructions[index] = mod, n
    return Program(instructions)

program = Program(parse(EXAMPLE_PROGRAM))
assert terminates(program) == False
assert terminates(modify_instruction(program, 0)) == False
assert terminates(modify_instruction(program, 7)) == True

def solve2(program):
    for index in range(len(program.instructions)):
        p = modify_instruction(program, index)
        if p is not None and terminates(p):
            #print(p.instructions)
            #print(index, p.accumulator)
            return p.accumulator
    assert False

assert solve2(program) == 8

with open('input') as f:
    program = Program(parse(f.read()))
print(solve1(program))
print(solve2(program))
