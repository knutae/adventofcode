
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

starting_positions = [2,7]
print(solve1(starting_positions))
