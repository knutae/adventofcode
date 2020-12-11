EXAMPLE = '''
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
'''

def step(input):
    lines = input.split('\n')
    width = len(lines[0])
    height = len(lines)

    def get(x,y):
        if x < 0 or x >= width or y < 0 or y >= height:
            return '.'
        return lines[y][x]

    def count_adjacent_occupied(x,y):
        count = 0
        for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
            if get(x+dx, y+dy) == '#':
                count += 1
        return count

    def new_tile(x,y):
        old_tile = get(x,y)
        if old_tile == '.':
            return '.'
        if old_tile == 'L':
            return '#' if count_adjacent_occupied(x,y) == 0 else 'L'
        if old_tile == '#':
            return 'L' if count_adjacent_occupied(x,y) >= 4 else '#'
        assert False

    return '\n'.join(
        ''.join(new_tile(x, y) for x in range(width))
        for y in range(height)
    )

def solve1(input):
    state = input.strip()
    #print(state + '\n')
    while True:
        new_state = step(state)
        #print(new_state + '\n')
        if new_state == state:
            return new_state.count('#')
        state = new_state

assert solve1(EXAMPLE) == 37

with open('input') as f:
    input = f.read().strip()

print(solve1(input))
