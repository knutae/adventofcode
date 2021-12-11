EXAMPLE = '''
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
'''

def parse_grid(data):
    lines = data.strip().split('\n')
    return [[int(c) for c in line] for line in lines]

def grid_str(grid):
    return '\n'.join(''.join(map(str,line)) for line in grid)

#grid = parse_grid(EXAMPLE)
#print(grid)
#print(grid_str(grid))

def adjacent(x, y):
    return [
        (x0,y0)
        for x0 in range(max(0, x-1), min(10, x+2))
        for y0 in range(max(0, y-1), min(10, y+2))
        if (x0,y0) != (x,y)
    ]

assert len(adjacent(3, 3)) == 8
assert len(adjacent(0, 3)) == 5
assert len(adjacent(0, 0)) == 3
assert len(adjacent(9, 9)) == 3

class Solver:
    def __init__(self, grid):
        assert len(grid) == 10 and len(grid[0]) == 10
        self.grid = grid
        self.flashes = 0

    def increment(self, x, y, flashes_this_step):
        grid = self.grid
        n = grid[y][x]
        assert n >= 0 and n <= 9
        if n == 0 and (x,y) in flashes_this_step:
            pass
        elif n < 9:
            grid[y][x] = n+1
        elif n == 9:
            assert (x,y) not in flashes_this_step
            flashes_this_step.add((x,y))
            self.flashes += 1
            grid[y][x] = 0
            for x0, y0 in adjacent(x, y):
                self.increment(x0, y0, flashes_this_step)

    def step(self):
        flashes_this_step = set()
        for y in range(10):
            for x in range(10):
                self.increment(x, y, flashes_this_step)
        return len(flashes_this_step)

def solve1(grid, steps=100, verbose=False):
    solver = Solver(grid)
    if verbose:
        print(f'Initial:\n{grid_str(solver.grid)}')
    for step in range(steps):
        solver.step()
        if verbose:
            print(f'\nStep {step+1}:\n{grid_str(solver.grid)}')
    return solver.flashes

def solve2(grid):
    solver = Solver(grid)
    steps = 0
    while True:
        steps += 1
        num_flashes = solver.step()
        if num_flashes == 100:
            return steps

assert solve1(parse_grid(EXAMPLE)) == 1656
assert solve2(parse_grid(EXAMPLE)) == 195

with open('input') as f:
    puzzle_input = f.read()

print(solve1(parse_grid(puzzle_input)))
print(solve2(parse_grid(puzzle_input)))
