EXAMPLE = '125 17'

def parse(data):
    return [int(x) for x in data.strip().split()]

def blink(stones):
    r = []
    for s in stones:
        ss = str(s)
        if s == 0:
            r.append(1)
        elif len(ss) % 2 == 0:
            split = len(ss) // 2
            r.append(int(ss[:split]))
            r.append(int(ss[split:]))
        else:
            r.append(s * 2024)
    return r

def solve1(data, steps=25):
    stones = parse(data)
    for _ in range(steps):
        stones = blink(stones)
        #print(stones)
    return len(stones)

assert solve1(EXAMPLE) == 55312

with open('input') as f:
    data = f.read()

print(solve1(data))
