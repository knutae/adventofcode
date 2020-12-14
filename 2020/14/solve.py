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

def apply_address_mask(mask, n):
    result = []
    for i, m in enumerate(reversed(mask)):
        if m == '0':
            result.append(str(1 & (n >> i)))
        else:
            assert m in '1X'
            result.append(m)
    result.reverse()
    return ''.join(result)

assert apply_address_mask('000000000000000000000000000000X1001X', 42) == '000000000000000000000000000000X1101X'

def generate_addresses(mask):
    i = mask.find('X')
    if i == -1:
        yield int(mask, 2)
    else:
        for c in '01':
            for address in generate_addresses(mask[:i] + c + mask[i+1:]):
                yield address

assert list(generate_addresses('000000000000000000000000000000X1101X')) == [26, 27, 58, 59]

EXAMPLE2 = '''
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
'''

def solve2(input):
    mask = None
    mem = dict()
    for a, b in parse(input):
        if a == 'mask':
            mask = b
        else:
            for address in generate_addresses(apply_address_mask(mask, a)):
                mem[address] = b
    return sum(mem.values())

assert solve2(EXAMPLE2) == 208

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
