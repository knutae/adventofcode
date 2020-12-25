
def transform(subject_number, loop_size):
    value = 1
    for i in range(loop_size):
        value *= subject_number
        value %= 20201227
    return value

assert transform(7, 8) == 5764801
assert transform(7, 11) == 17807724

def detect_loop_size(public_key, subject_number=7):
    value = 1
    i = 0
    while value != public_key:
        value *= subject_number
        value %= 20201227
        i += 1
    return i

assert detect_loop_size(5764801) == 8
assert detect_loop_size(17807724) == 11

def solve1(card_public_key, door_public_key):
    card_loop_size = detect_loop_size(card_public_key)
    door_loop_size = detect_loop_size(door_public_key)
    encryption_key = transform(card_public_key, door_loop_size)
    assert transform(door_public_key, card_loop_size) == encryption_key
    return encryption_key

assert solve1(5764801, 17807724) == 14897079

with open('input') as f:
    input = f.read()
[card_public_key, door_public_key] = [int(line) for line in input.strip().split('\n')]
print(solve1(card_public_key, door_public_key))
