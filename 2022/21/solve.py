EXAMPLE = '''
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
'''

def parse_line(line):
    [lhs, rhs] = line.split(': ')
    if rhs.isdigit():
        rhs = int(rhs)
    else:
        [a, op, b] = rhs.split()
        assert op in '+-*/'
        rhs = (a, op, b)
    return lhs, rhs

def parse(input):
    return [parse_line(line) for line in input.strip().split('\n')]

def solve1(input):
    table = dict(parse(input))
    memo = {}
    def rec_solve(name):
        assert name in table
        if name not in memo:
            expr = table[name]
            if isinstance(expr, int):
                value = expr
            else:
                a, op, b = expr
                a = rec_solve(a)
                b = rec_solve(b)
                if op == '+':
                    value = a + b
                elif op == '-':
                    value = a - b
                elif op == '*':
                    value = a * b
                elif op == '/':
                    assert a % b == 0
                    value = a // b
                else:
                    assert False
            memo[name] = value
        #print(f'{name} -> {memo[name]}')
        return memo[name]
    return rec_solve('root')

assert solve1(EXAMPLE) == 152

with open('input') as f:
    input = f.read()

print(solve1(input))
