EXAMPLE = '''
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
'''

def condition_to_func(condition):
    if '<' in condition:
        lhs, rhs = condition.split('<')
        rhs = int(rhs)
        return lambda part: part[lhs] < rhs
    if '>' in condition:
        lhs, rhs = condition.split('>')
        rhs = int(rhs)
        return lambda part: part[lhs] > rhs
    assert False

def condition_true(_):
    return True

def parse_expr(expr):
    if ':' in expr:
        condition, target = expr.split(':')
        condition = condition_to_func(condition)
        return condition, target
    else:
        return condition_true, expr

def parse_workflow(line):
    assert line[-1] == '}'
    name, expressions = line[:-1].split('{')
    expressions = expressions.split(',')
    return name, [parse_expr(expr) for expr in expressions]

def parse_part(line):
    assert line[0] == '{' and line[-1] == '}'
    r = dict()
    for chunk in line[1:-1].split(','):
        a,b = chunk.split('=')
        r[a] = int(b)
    return r

def parse(data):
    workflows, parts = data.strip().split('\n\n')
    workflows = dict(parse_workflow(line) for line in workflows.split('\n'))
    parts = [parse_part(line) for line in parts.split('\n')]
    return workflows, parts

def flow(part, workflows):
    current = 'in'
    while current not in ('R', 'A'):
        for condition, target in workflows[current]:
            if condition(part):
                current = target
                break
        else:
            assert False
    if current == 'A':
        return True
    else:
        assert current == 'R'
        return False

def solve1(data):
    workflows, parts = parse(data)
    accepted_parts = [part for part in parts if flow(part, workflows)]
    return sum(sum(part.values()) for part in accepted_parts)

assert solve1(EXAMPLE) == 19114

with open('input') as f:
    data = f.read()

print(solve1(data))
