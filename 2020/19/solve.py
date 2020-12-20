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

EXAMPLE_2 = '''
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
'''

def parse_input(input):
    [rules, messages] = input.strip().split('\n\n')
    return parse_rules(rules), messages.split('\n')

def generate_prefixed_messages(rules, rule_num, message):
    assert len(message) > 0
    for rule in rules[rule_num]:
        if isinstance(rule, str):
            if message.startswith(rule):
                yield rule
        else:
            assert isinstance(rule, list)
            assert len(rule) >= 1 and len(rule) <= 3
            for a in generate_prefixed_messages(rules, rule[0], message):
                assert message.startswith(a)
                #print(f"1! {a} (msg {message}, rule {rule})")
                if len(rule) == 1:
                    yield a
                    continue
                remaining_a = message[len(a):]
                if len(remaining_a) == 0:
                    continue
                for b in generate_prefixed_messages(rules, rule[1], remaining_a):
                    assert message.startswith(a + b)
                    #print(f"2! {a} {b} (msg {message}, rule {rule})")
                    if len(rule) == 2:
                        yield a + b
                        continue
                    remaining_ab = remaining_a[len(b):]
                    if len(remaining_ab) == 0:
                        continue
                    for c in generate_prefixed_messages(rules, rule[2], remaining_ab):
                        assert message.startswith(a + b + c)
                        #print(f"3! {a} {b} {c} (msg {message}, rule {rule})")
                        yield a + b + c

def matches_rule(rules, message, rule_num):
    for match in generate_prefixed_messages(rules, rule_num, message):
        if match == message:
            return True
    return False

def solve1(input):
    rules, messages = parse_input(input)
    matches = set()
    for i, message in enumerate(messages):
        #print(f'{i+1}/{len(messages)} {message}')
        if matches_rule(rules, message, 0):
            matches.add(message)
            #print('YES')
    #print(matches)
    return len(matches)

def solve2(input):
    rules, messages = parse_input(input)
    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]
    matches = set()
    for i, message in enumerate(messages):
        #print(f'{i+1}/{len(messages)} {message}')
        if matches_rule(rules, message, 0):
            matches.add(message)
    #print(matches)
    return len(matches)

assert solve1(EXAMPLE) == 2
assert solve1(EXAMPLE_2) == 3
assert solve2(EXAMPLE_2) == 12

with open('input') as f:
    input = f.read()
print(solve1(input))
print(solve2(input))
