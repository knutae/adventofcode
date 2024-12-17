EXAMPLE = '''
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
'''

class Computer:
    def __init__(self, registers, program):
        assert len(registers) == 3
        self.registers = list(registers)
        self.program = list(program)
        self.instruction_pointer = 0
        self.output = []
        self.instructions = [
            self.adv,
            self.bxl,
            self.bst,
            self.jnz,
            self.bxc,
            self.out,
            self.bdv,
            self.cdv,
        ]
    
    def literal_operand(self):
        return self.program[self.instruction_pointer + 1]

    def combo_operand(self):
        operand = self.literal_operand()
        if operand <= 3:
            return operand
        elif operand <= 6:
            return self.registers[operand - 4]
        else:
            assert False, f'invalid operand {operand}'

    def _dv(self, target_index):
        numerator = self.registers[0]
        denominator = 2**self.combo_operand()
        self.registers[target_index] = numerator // denominator
    
    def adv(self):
        self._dv(0)
    
    def bxl(self):
        self.registers[1] = self.registers[1] ^ self.literal_operand()
    
    def bst(self):
        self.registers[1] = self.combo_operand() % 8
    
    def jnz(self):
        if self.registers[0] != 0:
            # subtract 2 that will be added elsewhere
            self.instruction_pointer = self.literal_operand() - 2

    def bxc(self):
        self.registers[1] = self.registers[1] ^ self.registers[2]
    
    def out(self):
        self.output.append(self.combo_operand() % 8)
    
    def bdv(self):
        self._dv(1)
    
    def cdv(self):
        self._dv(2)

    def run_program(self):
        assert len(self.output) == 0
        assert self.instruction_pointer == 0
        while self.instruction_pointer < len(self.program):
            instruction = self.instructions[self.program[self.instruction_pointer]]
            instruction()
            self.instruction_pointer += 2

def run(registers, program):
    c = Computer(registers, program)
    c.run_program()
    #print(registers, program, "->", c.registers, c.output)
    return c

def test():
    assert run([0,0,9], [2,6]).registers == [0,1,9]
    assert run([10,0,0], [5,0,5,1,5,4]).output == [0,1,2]
    c = run([2024,0,0], [0,1,5,4,3,0])
    assert c.output == [4,2,5,6,7,7,7,7,3,1,0]
    assert c.registers == [0,0,0]

test()

def strip_prefix(line, prefix):
    assert line.startswith(prefix)
    return line[len(prefix):]

def parse_register(line, name):
    return int(strip_prefix(line, f'Register {name}: '))

def parse(data):
    registers, program = data.strip().split('\n\n')
    registers = registers.split('\n')
    assert len(registers) == 3
    registers = [parse_register(line, name) for line, name in zip(registers, 'ABC')]
    program = strip_prefix(program, 'Program: ')
    program = [int(x) for x in program.split(',')]
    return Computer(registers, program)

def solve1(data):
    c = parse(data)
    c.run_program()
    return ','.join(str(x) for x in c.output)

assert solve1(EXAMPLE) == '4,6,3,5,6,3,5,2,1,0'

with open('input') as f:
    data = f.read()

print(solve1(data))
