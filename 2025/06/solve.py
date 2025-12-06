import math

EXAMPLE = '''
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
'''

def parse(s):
    lines = s.strip().split('\n')
    numbers = [[int(x) for x in line.split()] for line in lines[:-1]]
    operators = lines[-1].split()
    return numbers, operators

def solve1(s):
    numbers, operators = parse(s)
    total = 0
    for i, op in enumerate(operators):
        col = [row[i] for row in numbers]
        if op == '+':
            total += sum(col)
        elif op == '*':
            total += math.prod(col)
        else:
            assert False
    return total

assert solve1(EXAMPLE) == 4277556

with open('input') as f:
    s = f.read()

print(solve1(s))
