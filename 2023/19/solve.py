import math

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

def parse_range_condition(condition):
    if '<' in condition:
        lhs, rhs = condition.split('<')
        rhs = int(rhs)
        return lhs, range(1, rhs)
    if '>' in condition:
        lhs, rhs = condition.split('>')
        rhs = int(rhs)
        return lhs, range(rhs, 4001)
    assert False

def parse_range_expr(expr):
    if ':' in expr:
        condition, target = expr.split(':')
        return parse_range_condition(condition), target
    else:
        return None, expr

def parse_range_workflow(line):
    assert line[-1] == '}'
    name, expressions = line[:-1].split('{')
    expressions = expressions.split(',')
    return name, [parse_range_expr(expr) for expr in expressions]

def parse2(data):
    workflows, _ = data.strip().split('\n\n')
    workflows = dict(parse_range_workflow(line) for line in workflows.split('\n'))
    return workflows

def exclude_one(r, exclude):
    if r.stop < exclude.start or r.start >= exclude.stop:
        return [r]
    result = []
    if r.start < exclude.start:
        result.append(range(r.start, exclude.start))
    if r.stop > exclude.stop:
        result.append(range(exclude.stop , r.stop))
    return result

def exclude_range(ranges, exclude):
    result = []
    for r in ranges:
        result.extend(exclude_one(r, exclude))
    return simplify_ranges(result)

def invert_ranges(ranges):
    if len(ranges) == 0:
        return [range(1, 4001)]
    inverted = []
    assert ranges[0].start >= 1
    assert ranges[-1].stop <= 4001
    inverted.append(range(1, ranges[0].start))
    for r1, r2 in zip(ranges, ranges[1:]):
        inverted.append(range(r1.stop, r2.start))
    inverted.append(range(r[-1].stop, 4001))
    return simplify_ranges(inverted)

def range_list_intersection(r1, r2):
    for i in invert_ranges(r2):
        r1 = exclude_range(r1, i)
    return r1

def remove_empty(range_list):
    return [r for r in range_list if len(r) > 0]

def restrict_ranges(condition, ranges):
    if condition is None:
        return ranges
    key, condition_range = condition
    ranges = dict(ranges)
    ranges[key] = remove_empty([range_intersection(r, condition_range) for r in ranges[key]])
    return ranges

def simplify_ranges(ranges):
    if len(ranges) == 0:
        return []
    ranges = list(sorted(ranges, key=lambda r: (r.start, r.stop)))
    result = [ranges[0]]
    for r in ranges[1:]:
        last = result[-1]
        if r.start > last.stop:
            result.append(r)
        else:
            result[-1] = range(last.start, max(r.stop, last.stop))
    return remove_empty(result)

#def range_union(ranges1, ranges2):
#    return simplify_ranges(ranges1 + ranges2)

def accepted_ranges(workflows, current, ranges):
    if current == 'R' or any(len(r) == 0 for r in ranges.values()):
        return {key: [] for key in ranges.keys()}
    if current == 'A':
        return ranges
    combined_ranges = {k: list(r) for k, r in ranges.items()} # deep copy
    for condition, target in workflows[current]:
        conditional_ranges = accepted_ranges(workflows, target, restrict_ranges(condition, ranges))
        combined_ranges = {k: remove_empty(range_intersection(v, conditional_ranges[k])) for k, v in combined_ranges.items()}
    return combined_ranges

def solve2(data):
    workflows = parse2(data)
    full_range = [range(1,4001)]
    full_ranges = {'x': full_range, 'm': full_range, 'a': full_range, 's': full_range}
    accepted = accepted_ranges(workflows, 'in', full_ranges)
    print(accepted)
    return math.prod(sum(len(r) for r in range_list) for range_list in accepted.values())

assert solve2(EXAMPLE) == 167409079868000

with open('input') as f:
    data = f.read()

print(solve1(data))
