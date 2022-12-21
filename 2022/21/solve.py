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

def safe_div(a, b):
    assert a % b == 0
    return a // b

OPS = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': safe_div,
}

def calculate(table, humn, variable):
    table['humn'] = humn
    def rec_solve(expr):
        if isinstance(expr, int):
            return expr
        assert expr in table
        expr = table[expr]
        if isinstance(expr, int):
            return expr
        a, op, b = expr
        a = rec_solve(a)
        b = rec_solve(b)
        return OPS[op](a, b)
    return rec_solve(variable)

def simplify(table):
    table = dict(table)
    inline = dict()
    while True:
        for name, expr in table.items():
            if isinstance(expr, int):
                inline[name] = expr
            else:
                a, op, b = expr
                if isinstance(a, int) and isinstance(b, int):
                    inline[name] = OPS[op](a, b)
        new_table = dict()
        modcount = 0
        for name, expr in table.items():
            if name in inline:
                modcount += 1
                continue
            a, op, b = expr
            if a in inline:
                modcount += 1
                a = inline[a]
            if b in inline:
                modcount += 1
                b = inline[b]
            new_table[name] = a, op, b
        table = new_table
        if modcount == 0:
            return table, inline

def solve1(input):
    table = dict(parse(input))
    table, inline = simplify(table)
    assert len(table) == 0
    return inline['root']

def is_valid(table, lhs, humn):
    table['humn'] = humn
    def rec_check(expr):
        if isinstance(expr, int):
            return expr
        assert expr in table
        expr = table[expr]
        if isinstance(expr, int):
            return expr
        a, op, b = expr
        a = rec_check(a)
        if a is None:
            return None
        b = rec_check(b)
        if b is None:
            return None
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if a % b != 0:
                # invalid division
                return None
            return a // b
        else:
            assert False
    return rec_check(lhs) is not None

def detect_start_and_incement(table, lhs):
    humn = 1
    samples = []
    while len(samples) < 10:
        if is_valid(table, lhs, humn):
            samples.append(humn)
        humn += 1
    start = samples[0]
    increment = samples[1] - samples[0]
    assert list(range(start, start + increment * 10, increment)) == samples
    return start, increment

def is_between(x, a, b):
    if a < b:
        return a <= x and x <= b
    if b < a:
        return b <= x and x <= a
    assert False

def solve2(input):
    table = dict(parse(input))
    lhs, _, rhs = table['root']
    del table['root']
    del table['humn']
    table, inline = simplify(table)
    assert rhs in inline
    rhs = inline[rhs]
    start, increment = detect_start_and_incement(table, lhs)
    # detect binary search range
    i = 1
    while True:
        min_i = i
        max_i = i*2
        min_lhs = calculate(table, start + min_i * increment, lhs)
        max_lhs = calculate(table, start + max_i * increment, lhs)
        if is_between(rhs, min_lhs, max_lhs):
            break
        i *= 2
    # binary search
    while True:
        i = (min_i + max_i) // 2
        humn = start + i * increment
        mid_lhs = calculate(table, humn, lhs)
        assert is_between(mid_lhs, min_lhs, max_lhs)
        if mid_lhs == rhs:
            return humn
        if is_between(rhs, min_lhs, mid_lhs):
            max_i = i
            max_lhs = mid_lhs
        else:
            assert is_between(rhs, mid_lhs, max_lhs)
            min_i = i
            min_lhs = mid_lhs

assert solve1(EXAMPLE) == 152
assert solve2(EXAMPLE) == 301

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
