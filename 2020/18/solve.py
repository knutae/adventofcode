def parenthesis_expression(expr, index):
    assert expr[index] == '('
    level = 1
    for i in range(index + 1, len(expr)):
        if expr[i] == '(':
            level += 1
        elif expr[i] == ')':
            level -= 1
            if level == 0:
                return expr[index+1:i]
    assert False

def parse_expression(expr):
    result = []
    index = 0
    while True:
        # read number or subexpression
        if expr[index] == '(':
            subexpr = parenthesis_expression(expr, index)
            assert expr[index + len(subexpr) + 1] == ')'
            result.append(parse_expression(subexpr))
            index += len(subexpr) + 2
        else:
            # read single digit number
            result.append(int(expr[index]))
            index += 1
        if index == len(expr):
            break
        assert expr[index] == ' '
        index += 1
        # read operator
        assert expr[index] in '+*'
        assert expr[index+1] == ' '
        result += expr[index]
        index += 2
    return result

assert parse_expression('1 + 2 * 3 + 4 * 5 + 6') == [1, '+', 2, '*', 3, '+', 4, '*', 5, '+', 6]
assert parse_expression('1 + (2 * 3) + (4 * (5 + 6))') == [1, '+', [2, '*', 3], '+', [4, '*', [5, '+', 6]]]

def eval_expression(expr):
    if isinstance(expr, int):
        return expr
    assert isinstance(expr, list)
    assert len(expr) % 2 == 1
    result = eval_expression(expr[0])
    for op, subexpr in zip(expr[1::2], expr[2::2]):
        n = eval_expression(subexpr)
        if op == '+':
            result += n
        elif op == '*':
            result *= n
        else:
            assert False
    return result

def eval1(line):
    return eval_expression(parse_expression(line))

assert eval1('1 + 2 * 3 + 4 * 5 + 6') == 71
assert eval1('1 + (2 * 3) + (4 * (5 + 6))') == 51
assert eval1('2 * 3 + (4 * 5)') == 26
assert eval1('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
assert eval1('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
assert eval1('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632

def solve1(input):
    return sum(eval1(line) for line in input.strip().split('\n'))

def force_precedence(expr):
    if isinstance(expr, int):
        return expr
    assert isinstance(expr, list)
    expr = [force_precedence(x) if isinstance(x, list) else x for x in expr]
    while len(expr) > 3 and '+' in expr:
        i = expr.index('+')
        new_subexpr = expr[i-1:i+2]
        assert len(new_subexpr) == 3 and new_subexpr[1] == '+'
        expr = expr[:i-1] + [new_subexpr] + expr[i+2:]
    assert len(expr) % 2 == 1
    return expr

def eval2(line):
    expr = parse_expression(line)
    expr = force_precedence(expr)
    return eval_expression(expr)

assert eval2('1 + 2 * 3 + 4 * 5 + 6') == 231
assert eval2('1 + (2 * 3) + (4 * (5 + 6))') == 51
assert eval2('2 * 3 + (4 * 5)') == 46
assert eval2('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 1445
assert eval2('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 669060
assert eval2('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 23340

def solve2(input):
    return sum(eval2(line) for line in input.strip().split('\n'))

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
