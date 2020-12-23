def parse(input):
    return [int(c) for c in input]

def previous_cup(cup):
    return 9 if cup == 1 else cup - 1

def step(cups):
    current = cups[0]
    removed_cups = cups[1:4]
    remaining = cups[4:]
    dest_cup = previous_cup(current)
    while dest_cup in removed_cups:
        dest_cup = previous_cup(dest_cup)
    dest_index = remaining.index(dest_cup) + 1
    # insert the removed cups after the destination, and move the current last
    # this makes the first cup the current for the next step
    new_cups = remaining[:dest_index] + removed_cups + remaining[dest_index:] + [current]
    return new_cups

assert step([3,8,9,1,2,5,4,6,7]) == [2,8,9,1,5,4,6,7,3]
assert step([2,8,9,1,5,4,6,7,3]) == [5,4,6,7,8,9,1,3,2]

def solve1(input, steps=100):
    cups = parse(input)
    for i in range(steps):
        cups = step(cups)
    index = cups.index(1)
    result = cups[index+1:] + cups[:index]
    return ''.join(str(n) for n in result)

assert solve1('389125467', 10) == '92658374'
assert solve1('389125467', 100) == '67384529'

print(solve1('496138527'))
