EXAMPLE = '''
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''

def parse_stacks(stacks):
    lines = stacks.split('\n')
    numbers_of_stacks = int(lines[-1].split()[-1])
    stacks = [[] for _ in range(numbers_of_stacks)]
    for line in reversed(lines[:-1]):
        for i, c in enumerate(line[1::4]):
            if c != ' ':
                stacks[i].append(c)
    return stacks

def parse_procedure(line):
    [_, n, _, source_stack, _, target_stack] = line.split()
    return int(n), int(source_stack), int(target_stack)

def parse_procedures(procedures):
    return [parse_procedure(line) for line in procedures.split('\n')]

def parse(input):
    stacks, procedures = input.strip('\n').split('\n\n')
    return parse_stacks(stacks), parse_procedures(procedures)

def move(stacks, count, source, target):
    for _ in range(count):
        stacks[target-1].append(stacks[source-1].pop())

def solve1(input):
    stacks, procedures = parse(input)
    for count, source, target in procedures:
        move(stacks, count, source, target)
    return ''.join(s[-1] for s in stacks)

def move2(stacks, count, source, target):
    stacks[target-1].extend(stacks[source-1][-count:])
    del stacks[source-1][-count:]

def solve2(input):
    stacks, procedures = parse(input)
    for count, source, target in procedures:
        move2(stacks, count, source, target)
    return ''.join(s[-1] for s in stacks)

assert solve1(EXAMPLE) == 'CMZ'
assert solve2(EXAMPLE) == 'MCD'

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
