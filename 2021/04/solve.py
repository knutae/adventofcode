EXAMPLE_INPUT='''7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
'''

def parse_board(input):
    lines = input.split('\n')
    return [[int(x) for x in line.split()] for line in lines]

def parse(input):
    parts = input.strip().split('\n\n')
    order = [int(x) for x in parts[0].split(',')]
    return order, [parse_board(x) for x in parts[1:]]

def board_wins(board, marked):
    for x in range(5):
        if all(board[x][y] in marked for y in range(5)) or all(board[y][x] in marked for y in range(5)):
            return True
    return False

def solve1(input):
    order, boards = parse(input)
    marked = set()
    for drawn in order:
        marked.add(drawn)
        winners = [b for b in boards if board_wins(b, marked)]
        if winners:
            assert len(winners) == 1
            winner = winners[0]
            unmarked_sum = sum(sum(x for x in line if x not in marked) for line in winner)
            #print(unmarked_sum, drawn)
            return unmarked_sum * drawn
    assert False

def solve2(input):
    order, boards = parse(input)
    marked = set()
    non_winners = boards
    for drawn in order:
        marked.add(drawn)
        assert len(non_winners) > 0
        if len(non_winners) == 1:
            # searching for the score of the last board
            last_board = non_winners[0]
            if board_wins(last_board, marked):
                unmarked_sum = sum(sum(x for x in line if x not in marked) for line in last_board)
                #print(unmarked_sum, drawn)
                return unmarked_sum * drawn
        else:
            non_winners = [b for b in non_winners if not board_wins(b, marked)]
    assert False

assert solve1(EXAMPLE_INPUT) == 4512
assert solve2(EXAMPLE_INPUT) == 1924

with open('input') as f:
    puzzle_input = f.read()

print(solve1(puzzle_input))
print(solve2(puzzle_input))
