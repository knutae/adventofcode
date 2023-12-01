EXAMPLE = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

EXAMPLE2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""


def solve1(data):
    lines = data.strip().split("\n")
    r = 0
    for line in lines:
        digits = [x for x in line if x.isdigit()]
        r += int(digits[0] + digits[-1])
    return r


DIGITS = {
    word: str(i + 1)
    for i, word in enumerate(
        ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    )
} | {str(i): str(i) for i in range(1, 10)}


def solve2(data):
    lines = data.strip().split("\n")
    r = 0
    for line in lines:
        first, last = (len(line), None), (-1, None)
        for word, i in DIGITS.items():
            lpos = line.find(word)
            if lpos != -1 and lpos < first[0]:
                assert lpos != first[0]
                first = lpos, i
            rpos = line.rfind(word)
            if rpos != -1 and rpos > last[0]:
                assert rpos != last[0]
                last = rpos, i
        #print(line, first, last)
        r += int(first[1] + last[1])
    return r


assert solve1(EXAMPLE) == 142
assert solve2(EXAMPLE2) == 281

with open("input") as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
