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

    def count_adjacent_occupied(x,y,limit):
        count = 0
        for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
            if get(x+dx, y+dy) == '#':
                count += 1
            if count >= limit:
                # optimization
                return count
        return count

    def new_tile(x,y):
        old_tile = get(x,y)
        if old_tile == '.':
            return '.'
        if old_tile == 'L':
            return '#' if count_adjacent_occupied(x,y,1) == 0 else 'L'
        if old_tile == '#':
            return 'L' if count_adjacent_occupied(x,y,4) >= 4 else '#'
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

def step2(input):
    lines = input.split('\n')
    width = len(lines[0])
    height = len(lines)

    def get(x,y):
        if x < 0 or x >= width or y < 0 or y >= height:
            return 'L'
        return lines[y][x]

    def can_see_occupied(x,y,dx,dy):
        while True:
            x += dx
            y += dy
            seen = get(x,y)
            if seen == 'L':
                return False
            if seen == '#':
                return True

    def count_seen_occupied(x,y,limit):
        count = 0
        for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
            if can_see_occupied(x, y, dx, dy):
                count += 1
            if count >= limit:
                # optimization
                return count
        return count

    def new_tile(x,y):
        old_tile = get(x,y)
        if old_tile == '.':
            return '.'
        if old_tile == 'L':
            return '#' if count_seen_occupied(x,y,1) == 0 else 'L'
        if old_tile == '#':
            return 'L' if count_seen_occupied(x,y,5) >= 5 else '#'
        assert False

    return '\n'.join(
        ''.join(new_tile(x, y) for x in range(width))
        for y in range(height)
    )

def solve2(input):
    state = input.strip()
    #print(state + '\n')
    while True:
        new_state = step2(state)
        #print(new_state + '\n')
        if new_state == state:
            return new_state.count('#')
        state = new_state

assert solve2(EXAMPLE) == 26

with open('input') as f:
    input = f.read().strip()

print(solve1(input))
print(solve2(input))
