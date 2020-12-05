
def seat_id(card):
    id = 0
    for c in card:
        id <<= 1
        if c in 'BR':
            id |= 1
    return id

assert seat_id('FBFBBFFRLR') == 357
assert seat_id('BFFFBBFRRR') == 567
assert seat_id('FFFBBBFRRR') == 119
assert seat_id('BBFFBBFRLL') == 820

with open('input') as f:
    cards = f.read().strip().split('\n')

ids = set(map(seat_id, cards))
print(max(ids))

candidates = set(range(min(ids), max(ids)+1))
print(candidates - ids)
