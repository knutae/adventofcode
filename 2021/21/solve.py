from collections import defaultdict

class Player:
    def __init__(self, position):
        self.position = position
        self.score = 0

    def move(self, amount):
        self.position = (self.position - 1 + amount) % 10 + 1
        self.score += self.position

def deterministic_dice():
    while True:
        for i in range(1,101):
            yield i

def solve1(starting_positions):
    player1 = Player(starting_positions[0])
    player2 = Player(starting_positions[1])
    dice = deterministic_dice()
    rolls = 0
    def roll():
        nonlocal rolls
        rolls += 3
        return next(dice) + next(dice) + next(dice)
    while player1.score < 1000 and player2.score < 1000:
        player1.move(roll())
        if player1.score < 1000:
            player2.move(roll())
    loser = player1 if player1.score < 1000 else player2
    return loser.score * rolls

assert solve1([4,8]) == 739785

def move(position, amount):
    return (position - 1 + amount) % 10 + 1

def quantum_dice_moves(position):
    # 1/1/1: 1 combo
    yield move(position, 3), 1
    # 1/1/2: 3 combos
    yield move(position, 4), 3
    # 1/2/2 and 1/1/3: 6 combos
    yield move(position, 5), 6
    # 2/2/2 and 1/2/3: 7 combos
    yield move(position, 6), 7
    # 2/2/3 and 1/3/3: 6 combos
    yield move(position, 7), 6
    # 2/3/3: 3 combos
    yield move(position, 8), 3
    # 3/3/3: 1 combo
    yield move(position, 9), 1

def quantum_step(universes):
    next_universes = defaultdict(int)
    for key, count in universes.items():
        a_turn, a_pos, a_score, b_pos, b_score = key
        assert a_score < 21 and b_score < 21
        if a_turn:
            for new_pos, new_count in quantum_dice_moves(a_pos):
                next_universes[(False, new_pos, a_score + new_pos, b_pos, b_score)] += count * new_count
        else:
            for new_pos, new_count in quantum_dice_moves(b_pos):
                next_universes[(True, a_pos, a_score, new_pos, b_score + new_pos)] += count * new_count
    return next_universes

def filter_winners(universes):
    remaining = dict()
    a_winners = 0
    b_winners = 0
    for key, count in universes.items():
        _, _, a_score, _, b_score = key
        if a_score >= 21:
            a_winners += count
        elif b_score >= 21:
            b_winners += count
        else:
            remaining[key] = count
    return a_winners, b_winners, remaining

def solve2(starting_positions):
    a, b = starting_positions
    universes = {(True, a, 0, b, 0): 1}
    total_a_winners = 0
    total_b_winners = 0
    while universes:
        universes = quantum_step(universes)
        a_winners, b_winners, universes = filter_winners(universes)
        total_a_winners += a_winners
        total_b_winners += b_winners
        #print(len(universes), a_winners, b_winners)
    #print(total_a_winners, total_b_winners)
    return max(total_a_winners, total_b_winners)

assert solve2([4,8]) == 444356092776315

starting_positions = [2,7]
print(solve1(starting_positions))
print(solve2(starting_positions))
