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

def solve2(s):
    rows = s.strip('\n').split('\n')
    cols = []
    for x in range(len(rows[0])-1, -1, -1):
        cols.append(''.join(row[x] for row in rows).strip())
    transposed = '\n'.join(cols)
    problems = transposed.split('\n\n')
    total = 0
    for problem in problems:
        lines = problem.split('\n')
        op = lines[-1][-1]
        lines[-1] = lines[-1][:-1] # oh so ugly
        numbers = [int(line) for line in lines]
        if op == '+':
            total += sum(numbers)
        elif op == '*':
            total += math.prod(numbers)
        else:
            assert False
    return total

assert solve2(EXAMPLE) == 3263827

with open('input') as f:
    s = f.read()

print(solve1(s))
print(solve2(s))
