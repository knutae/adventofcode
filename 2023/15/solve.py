EXAMPLE = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'

def HASH(s):
    h = 0
    for c in s:
        h = (h + ord(c)) * 17 % 256
    return h

assert HASH('HASH') == 52

def solve1(data):
    steps = data.strip().split(',')
    return sum(HASH(x) for x in steps)

assert solve1(EXAMPLE) == 1320

def solve2(data):
    steps = data.strip().split(',')
    boxes = [list() for _ in range(256)]
    for step in steps:
        if '=' in step:
            label, n = step.split('=')
            n = int(n)
            box = boxes[HASH(label)]
            existing = [i for i, x in enumerate(box) if x[0] == label]
            if existing:
                # replace existing
                assert len(existing) == 1
                box[existing[0]] = (label, n)
            else:
                # append
                box.append((label, n))
        else:
            assert step.endswith('-')
            label = step[:-1]
            h = HASH(label)
            boxes[h] = [(a, n) for a,n in boxes[h] if a != label]
    result = 0
    for i, box in enumerate(boxes):
        #if box:
        #    print(i, box)
        for j, lens in enumerate(box):
            result += (i+1) * (j+1) * lens[1]
    return result

assert solve2(EXAMPLE) == 145

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
