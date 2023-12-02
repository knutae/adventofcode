EXAMPLE = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

def parse_draw(data):
    parts = [x.split(' ') for x in  data.split(", ")]
    return {word[1]: int(word[0]) for word in parts}

def parse_game(line):
    [name, rest] = line.split(": ")
    parts = rest.split("; ")
    draws = [parse_draw(part) for part in parts]
    assert name.startswith("Game ")
    id = int(name[len("Game "):])
    return id, draws

def parse(data):
    return [parse_game(line) for line in data.strip().split("\n")]

#print(parse(EXAMPLE))

def possible_draw(draw):
    return draw.get('red', 0) <= 12 and draw.get('green', 0) <= 13 and draw.get('blue', 0) <= 14

def solve1(data):
    games = parse(data)
    r = 0
    for id, draws in games:
        if all(possible_draw(draw) for draw in draws):
            r += id
    return r

assert solve1(EXAMPLE) == 8

with open('input') as f:
    data = f.read()

print(solve1(data))
