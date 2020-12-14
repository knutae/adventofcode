EXAMPLE = '''
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
'''

def parse_line(line):
    [lhs, rhs] = line.split(' = ')
    if lhs == 'mask':
        assert len(rhs) == 36
        return lhs, rhs
    assert lhs.startswith('mem[') and lhs.endswith(']')
    address = int(lhs[4:-1])
    value = int(rhs)
    return address, value

def parse(input):
    return [parse_line(line) for line in input.strip().split('\n')]

def apply_mask(mask, n):
    # there should be a way more efficient way to do this...
    for i, m in enumerate(reversed(mask)):
        if m == '1':
            n |= 1 << i
        elif m == '0':
            n &= ~(1 << i)
        else:
            assert m == 'X'
    return n

assert apply_mask('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 11) == 73
assert apply_mask('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 101) == 101
assert apply_mask('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 0) == 64

def solve1(input):
    mask = None
    mem = dict()
    for a, b in parse(input):
        if a == 'mask':
            mask = b
        else:
            mem[a] = apply_mask(mask, b)
    return sum(mem.values())

assert solve1(EXAMPLE) == 165

with open('input') as f:
    input = f.read()

print(solve1(input))
