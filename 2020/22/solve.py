EXAMPLE = '''
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
'''

def parse(input):
    [p1, p2] = input.strip().split('\n\n')
    p1 = p1.split('\n')
    assert p1[0] == 'Player 1:'
    p2 = p2.split('\n')
    assert p2[0] == 'Player 2:'
    return [int(x) for x in p1[1:]], [int(x) for x in p2[1:]]

def play_round(p1, p2, verbose=False):
    winner = max(p1, p2, key=lambda p:p[0])
    loser = min(p1, p2, key=lambda p:p[0])
    if verbose:
        print(f"Player 1's deck: {', '.join(map(str, p1))}")
        print(f"Player 2's deck: {', '.join(map(str, p2))}")
        print(f"Player 1 plays: {p1[0]}")
        print(f"Player 2 plays: {p2[0]}")
        print(f"Player {1 if winner == p1 else 2} wins the round!")
    high = winner[0]
    low = loser[0]
    del winner[0]
    del loser[0]
    winner.append(high)
    winner.append(low)

def solve1(input, verbose=False):
    p1, p2 = parse(input)
    round = 1
    while len(p1) > 0 and len(p2) > 0:
        if verbose:
            print(f'\n-- Round {round} --')
        play_round(p1, p2, verbose)
        round += 1
    if verbose:
        print('\n== Post-game results ==')
        print(f"Player 1's deck: {', '.join(map(str, p1))}")
        print(f"Player 2's deck: {', '.join(map(str, p2))}")
    cards = p1 + p2
    score = sum(card * n for card, n in zip(cards, range(len(cards), 0, -1)))
    if verbose:
        print(f"Score: {score}")
    return score

assert solve1(EXAMPLE) == 306

with open('input') as f:
    input = f.read()
print(solve1(input))
