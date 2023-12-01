EXAMPLE = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

def solve1(data):
    lines = data.strip().split("\n")
    r = 0
    for line in lines:
        digits = [x for x in line if x.isdigit()]
        r += int(digits[0] + digits[-1])
    return r

assert solve1(EXAMPLE) == 142

with open('input') as f:
    data = f.read()

print(solve1(data))
