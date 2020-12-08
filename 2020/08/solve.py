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
    def __init__(self, input):
        self.instructions = parse(input)
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

def solve1(program):
    visited = set()
    while program.instruction_pointer not in visited:
        visited.add(program.instruction_pointer)
        program.step()
    return program.accumulator

assert solve1(Program(EXAMPLE_PROGRAM)) == 5

with open('input') as f:
    program = Program(f.read())
print(solve1(program))
