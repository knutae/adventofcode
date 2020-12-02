TEST_INPUT = '''
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
'''

def parse_line(line):
    [policy, password] = line.strip().split(': ')
    [policy_range, letter] = policy.split(' ')
    [rstart, rend] = policy_range.split('-')
    return int(rstart), int(rend), letter, password

def parse(lines):
    return [parse_line(line) for line in lines.strip().split('\n')]

def solve1(input):
    valid = 0
    invalid = 0
    for (rstart, rend, letter, password) in input:
        if password.count(letter) in range(rstart, rend+1):
            valid += 1
        else:
            invalid += 1
    #print(valid, invalid)
    return valid

assert parse_line('1-3 a: abcde') == (1, 3, 'a', 'abcde')
assert solve1(parse(TEST_INPUT)) == 2
with open('input') as f:
    input = parse(f.read())
print(solve1(input))
