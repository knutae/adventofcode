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

with open('input') as f:
    data = f.read()

print(solve1(data))
