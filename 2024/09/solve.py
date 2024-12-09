EXAMPLE = '2333133121414131402'

def parse(data):
    return [int(x) for x in data.strip()]

def expand_blocks(format):
    r = []
    for i, n in enumerate(format):
        if i % 2 == 0:
            id = i // 2
            r.extend([id] * n)
        else:
            r.extend([None] * n)
    return r

def defrag(blocks):
    blocks = list(blocks)
    a = 0
    b = len(blocks)-1
    while True:
        while blocks[a] is not None:
            a += 1
        while blocks[b] is None:
            b -= 1
        if a >= b:
            return blocks[:a]
        blocks[a] = blocks[b]
        blocks[b] = None

def checksum(blocks):
    return sum(i * n for i, n in enumerate(blocks))

def solve1(data):
    return checksum(defrag(expand_blocks(parse(data))))

assert solve1(EXAMPLE) == 1928

with open('input') as f:
    data = f.read()

print(solve1(data))
