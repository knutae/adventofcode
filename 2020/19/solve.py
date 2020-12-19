def parse_subrule(s):
    assert '|' not in s
    if s.startswith('"'):
        # literal string
        assert s.endswith('"')
        return s[1:-1]
    else:
        # list of rule numbers
        return [int(x) for x in s.split(' ')]

def parse_rule(s):
    [num, rest] = s.split(': ')
    num = int(num)
    return num, [parse_subrule(x) for x in rest.split(' | ')]

def parse_rules(s):
    return dict(parse_rule(r) for r in s.strip().split('\n'))

EXAMPLE = '''
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
'''

def parse_input(input):
    [rules, messages] = input.strip().split('\n\n')
    return parse_rules(rules), messages.split('\n')

RULES_EXAMPLE_1 = '''
0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"
'''

def generate_all_messages(rules, rule_num):
    for rule in rules[rule_num]:
        if isinstance(rule, str):
            yield rule
        else:
            assert isinstance(rule, list)
            assert len(rule) >= 1 and len(rule) <= 3
            for a in generate_all_messages(rules, rule[0]):
                if len(rule) == 1:
                    yield a
                else:
                    for b in generate_all_messages(rules, rule[1]):
                        if len(rule) == 2:
                            yield a + b
                        else:
                            for c in generate_all_messages(rules, rule[2]):
                                yield a + b + c

def solve1(input):
    rules, messages = parse_input(input)
    messages = set(messages)
    matches = set()
    for message in generate_all_messages(rules, 0):
        if message in messages:
            matches.add(message)
    #print(matches)
    return len(matches)

assert solve1(EXAMPLE) == 2

with open('input') as f:
    input = f.read()
print(solve1(input))
