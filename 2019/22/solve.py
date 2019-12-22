import sys

def deal_into_new_stack(cards):
    return cards[::-1]

def cut_cards(cards, n):
    return cards[n:] + cards[:n]

def deal_with_increment(cards, n):
    r = [None]*len(cards)
    for i, c in enumerate(cards):
        r[i*n % len(cards)] = c
    return r

def run_command(cards, command):
    if command == 'deal into new stack':
        return deal_into_new_stack(cards)
    if command.startswith('cut '):
        n = int(command[len('cut '):])
        return cut_cards(cards, n)
    if command.startswith('deal with increment '):
        n = int(command[len('deal with increment '):])
        return deal_with_increment(cards, n)
    assert False

def shuffle(cards, commands):
    for command in commands:
        cards = run_command(cards, command)
    return cards

def test():
    cards = [0,1,2,3,4,5,6,7,8,9]
    assert cut_cards(cards, 3) == [3,4,5,6,7,8,9,0,1,2]
    assert cut_cards(cards, -4) == [6,7,8,9,0,1,2,3,4,5]
    assert deal_with_increment(cards, 3) == [0,7,4,1,8,5,2,9,6,3]
    assert shuffle(cards, [
        'deal with increment 7',
        'deal into new stack',
        'deal into new stack',
    ]) == [0,3,6,9,2,5,8,1,4,7]
    assert shuffle(cards, [
        'cut 6',
        'deal with increment 7',
        'deal into new stack',
    ]) == [3,0,7,4,1,8,5,2,9,6]
    assert shuffle(cards, [
        'deal with increment 7',
        'deal with increment 9',
        'cut -2',
    ]) == [6,3,0,7,4,1,8,5,2,9]
    assert shuffle(cards, [
        'deal into new stack',
        'cut -2',
        'deal with increment 7',
        'cut 8',
        'cut -4',
        'deal with increment 7',
        'cut 3',
        'deal with increment 9',
        'deal with increment 3',
        'cut -1',
    ]) == [9,2,5,8,1,4,7,0,3,6]

test()

def main():
    cards = list(range(10007))
    with open('input') as f:
        commands = f.read().strip().split('\n')
    cards = shuffle(cards, commands)
    print(cards.index(2019))

main()