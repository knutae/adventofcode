EXAMPLE = '''
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
'''

CLOSING_CHARS = {')': '(', '}': '{', ']': '[', '>': '<'}
AUTOCOMPLETE_CHARS = {v: k for k, v in CLOSING_CHARS.items()}

def first_illegal_char(line):
    stack = []
    for c in line:
        if c in '([{<':
            stack.append(c)
            continue
        if len(stack) == 0 or CLOSING_CHARS[c] != stack[-1]:
            return c
        stack.pop()
    return None

def solve1(data):
    scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
    lines = data.strip().split('\n')
    return sum(scores.get(first_illegal_char(line), 0) for line in lines)

def autocomplete(line):
    stack = []
    for c in line:
        if c in '([{<':
            stack.append(c)
            continue
        assert len(stack) > 0 and CLOSING_CHARS[c] == stack[-1]
        stack.pop()
    return ''.join(AUTOCOMPLETE_CHARS[c] for c in reversed(stack))

def autocomplete_score(s):
    score = 0
    char_scores = {')': 1, ']': 2, '}': 3, '>': 4}
    for c in s:
        score = score * 5 + char_scores[c]
    return score

def solve2(data):
    lines = data.strip().split('\n')
    lines = [line for line in lines if first_illegal_char(line) is None]
    scores = [autocomplete_score(autocomplete(line)) for line in lines]
    scores.sort()
    assert len(scores) % 2 == 1
    return scores[len(scores) // 2]

assert solve1(EXAMPLE) == 26397
assert solve2(EXAMPLE) == 288957

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
