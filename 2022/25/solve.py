EXAMPLE = '''
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
'''

def snafu_digit(c):
    return '=-012'.index(c) - 2

def parse_snafu(s):
    return sum(snafu_digit(c) * 5**i for i, c in enumerate(reversed(s)))

def parse(input):
    return [parse_snafu(s) for s in input.strip().split('\n')]

def to_snafu(n):
    if n == 0:
        # return empty string to simplify recursive logic
        return ''
    assert n > 0
    d = n % 5
    if d <= 2:
        return to_snafu(n // 5) + str(d)
    if d == 3:
        return to_snafu((n + 2) // 5) + '='
    if d == 4:
        return to_snafu((n + 1) // 5) + '-'
    assert False

assert to_snafu(1) == '1'
assert to_snafu(2) == '2'
assert to_snafu(3) == '1='
assert to_snafu(4) == '1-'
assert to_snafu(5) == '10'
assert to_snafu(6) == '11'
assert to_snafu(7) == '12'
assert to_snafu(8) == '2='
assert to_snafu(9) == '2-'
assert to_snafu(10) == '20'
assert to_snafu(15) == '1=0'
assert to_snafu(2022) == '1=11-2'
assert to_snafu(12345) == '1-0---0'
assert to_snafu(314159265) == '1121-1110-1=0'

def solve(input):
    return to_snafu(sum(parse(input)))

assert solve(EXAMPLE) == '2=-1=0'

with open('input') as f:
    input = f.read()

print(solve(input))
