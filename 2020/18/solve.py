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

def eval_line(line):
    return eval_expression(parse_expression(line))

assert eval_line('1 + 2 * 3 + 4 * 5 + 6') == 71
assert eval_line('1 + (2 * 3) + (4 * (5 + 6))') == 51
assert eval_line('2 * 3 + (4 * 5)') == 26
assert eval_line('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
assert eval_line('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
assert eval_line('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632

def solve1(input):
    return sum(eval_line(line) for line in input.strip().split('\n'))

with open('input') as f:
    input = f.read()

print(solve1(input))
