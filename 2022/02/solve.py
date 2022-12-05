def solve1(input):
    score = 0
    for line in input.strip().split('\n'):
        [opponent, response] = line.split()
        opponent = ord(opponent) - ord('A')
        response = ord(response) - ord('X')
        score += response + 1
        if opponent == response:
            # draw
            score += 3
        elif (response - opponent) % 3 == 1:
            # win
            score += 6
        else:
            # loss
            assert (response - opponent) % 3 == 2
    return score

def solve2(input):
    score = 0
    for line in input.strip().split('\n'):
        [opponent, result] = line.split()
        opponent = ord(opponent) - ord('A')
        if result == 'X':
            # lose
            response = (opponent + 2) % 3
        elif result == 'Y':
            # draw
            response = opponent
            score += 3
        else:
            # win
            assert result == 'Z'
            response = (opponent + 1) % 3
            score += 6
        score += response + 1
    return score

assert solve1('A Y\nB X\nC Z') == 15
assert solve2('A Y\nB X\nC Z') == 12

with open('input') as f:
    input = f.read()
    print(solve1(input))
    print(solve2(input))
