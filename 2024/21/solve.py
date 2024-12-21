EXAMPLE = '''
029A
980A
179A
456A
379A
'''

NUMPAD = [
    '789',
    '456',
    '123',
    '.0A',
]

DIRPAD = [
    '.^A',
    '<v>',
]

def pad_position(pad, c):
    for y, line in enumerate(pad):
        for x, b in enumerate(line):
            if b == c:
                return x,y
    assert False

def moves(from_pos, to_pos, pad):
    from_x, from_y = from_pos
    to_x, to_y = to_pos
    horizontal_char = '<' if to_x < from_x else '>'
    horizontal = horizontal_char * abs(to_x - from_x)
    vertical_char = '^' if to_y < from_y else 'v'
    vertical = vertical_char * abs(to_y - from_y)
    if not horizontal:
        return vertical
    if not vertical:
        return horizontal
    # choose the order of hotizontal/vertical moves to avoid the empty pad
    # but we also want to end up close to the A on the directional pad to minimize the length...
    bad_pos = pad_position(pad, '.')
    if horizontal_char == '<':
        if (to_x, from_y) == bad_pos:
            # going left first is not possible
            return vertical + horizontal
        else:
            return horizontal + vertical
    if vertical_char == 'v':
        if (from_x, to_y) == bad_pos:
            # going down first is not possible
            return horizontal + vertical
        else:
            return vertical + horizontal
    assert horizontal_char == '>' and vertical_char == '^'
    # the order of right and up moves should not matter
    return horizontal + vertical    

def pad_moves(pad, code):
    assert code.endswith('A')
    all_moves = []
    pos = pad_position(pad, 'A')
    for c in code:
        to_pos = pad_position(pad, c)
        all_moves.append(moves(pos, to_pos, pad) + 'A')
        pos = to_pos
    return ''.join(all_moves)

assert pad_moves(NUMPAD, '029A') == '<A^A>^^AvvvA'

def triple_pad_moves(code):
    code = pad_moves(NUMPAD, code)
    for _ in range(2):
        code = pad_moves(DIRPAD, code)
    return code

assert len(triple_pad_moves('029A')) == 68
assert len(triple_pad_moves('980A')) == 60
assert len(triple_pad_moves('179A')) == 68

def solve1(data):
    codes = data.strip().split('\n')
    r = 0
    for code in codes:
        length = len(triple_pad_moves(code))
        numeric = int(code[0:3])
        #print(length, numeric)
        r += length * numeric
    return r

assert solve1(EXAMPLE) == 126384

with open('input') as f:
    data = f.read()

print(solve1(data))
