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

LOOPING_EXAMPLE = '''
Player 1:
43
19

Player 2:
2
29
14
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

def play_game(p1, p2, verbose=False):
    round = 1
    previous_game_positions = set()
    while len(p1) > 0 and len(p2) > 0:
        if verbose:
            print(f'\n-- Round {round} --')
        play_round(p1, p2, verbose)
        round += 1
        game_position = tuple(p1), tuple(p2)
        if game_position in previous_game_positions:
            if verbose:
                print(f"Game position repeated, declaring player 1 the winner")
            return 1
        previous_game_positions.add(game_position)
    if verbose:
        print('\n== Post-game results ==')
        print(f"Player 1's deck: {', '.join(map(str, p1))}")
        print(f"Player 2's deck: {', '.join(map(str, p2))}")
    winner = 1 if len(p2) == 0 else 2
    return winner

def solve1(input, verbose=False):
    p1, p2 = parse(input)
    winner = play_game(p1, p2, verbose)
    cards = p1 + p2
    score = sum(card * n for card, n in zip(cards, range(len(cards), 0, -1)))
    return score

def play_recursive_round(p1, p2, game_num, game_num_generator, verbose=False):
    if verbose:
        print(f"Player 1's deck: {', '.join(map(str, p1))}")
        print(f"Player 2's deck: {', '.join(map(str, p2))}")
        print(f"Player 1 plays: {p1[0]}")
        print(f"Player 2 plays: {p2[0]}")
    if len(p1) > p1[0] and len(p2) > p2[0]:
        # recursive sub-game
        if verbose:
            print("Playing a sub-game to determine the winner...")
        winning_player = play_recursive_game(p1[1:p1[0]+1], p2[1:p2[0]+1], game_num_generator=game_num_generator, verbose=verbose)
        if verbose:
            print(f"...anyway, back to game {game_num}.")
    else:
        # no recursion, highest card wins
        winning_player = 1 if p1[0] > p2[0] else 2
    assert winning_player == 1 or winning_player == 2
    winner = p1 if winning_player == 1 else p2
    loser = p2 if winning_player == 1 else p1
    first = winner[0]
    second = loser[0]
    del winner[0]
    del loser[0]
    winner.append(first)
    winner.append(second)
    return winning_player

def positive_integers():
    n = 0
    while True:
        n += 1
        yield n

def play_recursive_game(p1, p2, game_num_generator=None, verbose=False):
    assert len(p1) > 0 and len(p2) > 0
    if game_num_generator is None:
        game_num_generator = positive_integers()
    game_num = next(game_num_generator)
    round = 1
    previous_game_positions = set()
    while len(p1) > 0 and len(p2) > 0:
        if verbose:
            print(f'\n-- Round {round} (game {game_num}) --')
        winning_player = play_recursive_round(p1, p2, game_num, game_num_generator, verbose=verbose)
        if verbose:
            print(f"Player {winning_player} wins round {round} of game {game_num}!")
        round += 1
        game_position = tuple(p1), tuple(p2)
        if game_position in previous_game_positions:
            if verbose:
                print(f"Game position repeated, declaring player 1 the winner")
            return 1
        previous_game_positions.add(game_position)
    winner = 1 if len(p2) == 0 else 2
    return winner

def solve2(input, verbose=False):
    p1, p2 = parse(input)
    play_recursive_game(p1, p2, verbose=verbose)
    cards = p1 + p2
    score = sum(card * n for card, n in zip(cards, range(len(cards), 0, -1)))
    if verbose:
        print('\n== Post-game results ==')
        print(f"Player 1's deck: {', '.join(map(str, p1))}")
        print(f"Player 2's deck: {', '.join(map(str, p2))}")
        print(f'Score: {score}')
    return score

assert solve1(EXAMPLE) == 306
solve1(LOOPING_EXAMPLE) # smoke test
assert solve2(EXAMPLE) == 291

with open('input') as f:
    input = f.read()
print(solve1(input))
print(solve2(input))
