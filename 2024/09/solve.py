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
            return blocks
        blocks[a] = blocks[b]
        blocks[b] = None

def checksum(blocks):
    return sum(i * n for i, n in enumerate(blocks) if n is not None)

def solve1(data):
    return checksum(defrag(expand_blocks(parse(data))))

def find_free_space(blocks, n, end):
    free_count = 0
    for i in range(end):
        if blocks[i] is None:
            free_count += 1
            if free_count == n:
                return i - n + 1
        else:
            free_count = 0
    return None

def defrag_files(blocks):
    blocks = list(blocks)
    max_id = max(n for n in blocks if n is not None)
    for id in range(max_id, -1, -1):
        # detecting the index and file size could be much faster...
        file_index = blocks.index(id)
        file_size = blocks.count(id)
        free_index = find_free_space(blocks, file_size, file_index)
        if free_index is not None:
            for i in range(file_size):
                assert blocks[file_index + i] == id
                assert blocks[free_index + i] == None
                blocks[free_index + i] = id
                blocks[file_index + i] = None
    return blocks

def solve2(data):
    return checksum(defrag_files(expand_blocks(parse(data))))

assert solve1(EXAMPLE) == 1928
assert solve2(EXAMPLE) == 2858

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
