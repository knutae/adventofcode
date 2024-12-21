from collections import Counter

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

def pad_position_map(pad):
    r = {}
    for y, line in enumerate(pad):
        for x, c in enumerate(line):
            r[c] = (x,y)
    return r

NUMPAD_POSITIONS = pad_position_map(NUMPAD)
DIRPAD_POSITIONS = pad_position_map(DIRPAD)

def pad_position(pad, c):
    for y, line in enumerate(pad):
        for x, b in enumerate(line):
            if b == c:
                return x,y
    assert False

def moves(from_pos, to_pos, pad_positions):
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
    bad_pos = pad_positions['.']
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
    # '>' and '^' are both one move away from 'A', so I first thought the order didn't matter.
    # However, doing '^' first is still better since going left first leads to fewer moves on
    # the outer directional pad. Phew, this is complicated!
    if (from_x, to_y) == bad_pos:
        # going up first is not possible
        return horizontal + vertical
    else:
        return vertical + horizontal

def pad_moves(pad_positions, code):
    assert code.endswith('A')
    all_moves = []
    pos = pad_positions['A']
    for c in code:
        to_pos = pad_positions[c]
        all_moves.append(moves(pos, to_pos, pad_positions))
        all_moves.append('A')
        pos = to_pos
    return ''.join(all_moves)

assert pad_moves(NUMPAD_POSITIONS, '029A') == '<A^A^^>AvvvA'

def triple_pad_moves(code):
    code = pad_moves(NUMPAD_POSITIONS, code)
    for _ in range(2):
        code = pad_moves(DIRPAD_POSITIONS, code)
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
        r += length * numeric
    return r

assert solve1(EXAMPLE) == 126384

def split_moves(moves):
    chunks = Counter()
    index = 0
    while index < len(moves):
        end_index = moves.index('A', index) + 1
        chunk = moves[index:end_index]
        chunks[chunk] += 1
        index = end_index
    assert index == len(moves)
    return chunks

def multi_pad_chunk_lengths(code, robots):
    code = pad_moves(NUMPAD_POSITIONS, code)
    chunks = split_moves(code)
    for _ in range(robots):
        next_chunks = Counter()
        for chunk, count in chunks.items():
            for next_chunk, next_count in split_moves(pad_moves(DIRPAD_POSITIONS, chunk)).items():
                next_chunks[next_chunk] += count * next_count
        chunks = next_chunks
    return sum(len(chunk)*count for chunk, count in chunks.items())

def solve2(data, robots=25):
    codes = data.strip().split('\n')
    r = 0
    for code in codes:
        length = multi_pad_chunk_lengths(code, robots)
        numeric = int(code[0:3])
        r += length * numeric
    return r

assert solve2(EXAMPLE, 2) == 126384

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
