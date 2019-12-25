class Grid:
    def __init__(self, width, height, data):
        assert len(data) == width * height
        self.width = width
        self.height = height
        self.data = data

    def get(self, x, y):
        return self.data[y*self.width + x]

    def has_bug(self, x, y):
        return self.get(x, y) == '#'

    def count_adjacent_bugs(self, x, y):
        count = 0
        if y > 0:
            count += self.has_bug(x, y-1)
        if y < self.height - 1:
            count += self.has_bug(x, y+1)
        if x > 0:
            count += self.has_bug(x-1, y)
        if x < self.width - 1:
            count += self.has_bug(x+1, y)
        #print(f'adjacent {x} {y} -> {count}')
        return count

    def next_generation(self):
        new_data = [None]*len(self.data)
        for y in range(self.height):
            for x in range(self.width):
                is_bug = self.has_bug(x, y)
                count = self.count_adjacent_bugs(x, y)
                if is_bug:
                    is_new_bug = count == 1
                else:
                    is_new_bug = count in [1,2]
                new_data[y*self.width + x] = '#' if is_new_bug else '.'
        return ''.join(new_data)

    def print_grid(self):
        print('\n'.join(self.data[self.width*y:self.width*(y+1)] for y in range(self.height)))

    def biodiversity_rating(self):
        rating = 0
        n = 1
        for c in self.data:
            if c == '#':
                rating += n
            n <<= 1
        return rating

def parse_grid(data):
    lines = data.strip().split('\n')
    width = len(lines[0])
    height = len(lines)
    return Grid(width, height, ''.join(lines))

def iterate_until_seen_twice(grid):
    seen = set()
    while grid.data not in seen:
        seen.add(grid.data)
        grid.data = grid.next_generation()

class RecursiveGrid:
    def __init__(self, data):
        assert len(data) == 25
        self.levels = dict()
        self.levels[0] = data

    def get(self, level, x, y):
        return self.levels[level][y*5 + x]

    def has_bug(self, level, x, y):
        assert x >= 0 and x <= 4
        assert y >= 0 and y <= 4
        assert x != 2 or y != 2
        return level in self.levels and self.get(level, x, y) == '#'

    def _count_left(self, level):
        return sum(self.has_bug(level, 0, y) for y in range(5))
    
    def _count_right(self, level):
        return sum(self.has_bug(level, 4, y) for y in range(5))

    def _count_top(self, level):
        return sum(self.has_bug(level, x, 0) for x in range(5))

    def _count_bottom(self, level):
        return sum(self.has_bug(level, x, 4) for x in range(5))

    def count_adjacent_bugs(self, level, x, y):
        count = 0

        # Left
        if x == 0:
            # outer (level-1) cell at (1,2)
            count += self.has_bug(level-1, 1, 2)
        elif x == 3 and y == 2:
            # inner (level+1) cells at the right edge
            count += self._count_right(level+1)
        else:
            # same level
            count += self.has_bug(level, x-1, y)

        # Right
        if x == 4:
            # outer (level-1) cell at (3,2)
            count += self.has_bug(level-1, 3, 2)
        elif x == 1 and y == 2:
            # inner (level+1) cells at the left edge
            count += self._count_left(level+1)
        else:
            # same level
            count += self.has_bug(level, x+1, y)

        # Up
        if y == 0:
            # outer (level-1) cell at (2,1)
            count += self.has_bug(level-1, 2, 1)
        elif y == 3 and x == 2:
            # inner (level+1) cells at the bottom edge
            count += self._count_bottom(level+1)
        else:
            # same level
            count += self.has_bug(level, x, y-1)
        
        # Down
        if y == 4:
            # outer (level-1) cell at (2,3)
            count += self.has_bug(level-1, 2, 3)
        elif y == 1 and x == 2:
            # inner (level+1) cells at the top edge
            count += self._count_top(level+1)
        else:
            # same level
            count += self.has_bug(level, x, y+1)

        #print(f'adjacent {x} {y} -> {count}')
        return count

    def next_generation_for_level(self, level):
        new_data = [None]*25
        bug_count = 0
        for y in range(5):
            for x in range(5):
                if x == 2 and y == 2:
                    new_data[y*5 + x] = '?'
                    continue
                is_bug = self.has_bug(level, x, y)
                count = self.count_adjacent_bugs(level, x, y)
                if is_bug:
                    is_new_bug = count == 1
                else:
                    is_new_bug = count in [1,2]
                new_data[y*5 + x] = '#' if is_new_bug else '.'
                if is_new_bug:
                    bug_count += 1
        if bug_count == 0:
            return None
        else:
            return ''.join(new_data)    

    def next_generation(self):
        new_levels = dict()
        for level in range(min(self.levels.keys()) - 1, max(self.levels.keys()) + 2):
            new_level = self.next_generation_for_level(level)
            if new_level is not None:
                new_levels[level] = new_level
        return new_levels

    def print_grids(self):
        for level in range(min(self.levels.keys()), max(self.levels.keys()) + 1):
            print(f'Depth {level}:')
            if level in self.levels:
                print('\n'.join(self.levels[level][5*y:5*(y+1)] for y in range(5)) + '\n')
            else:
                print('(Empty level)\n')

    def total_bug_count(self):
        return sum(data.count('#') for data in self.levels.values())

def parse_recursive_grid(data):
    lines = data.strip().split('\n')
    assert len(lines[0]) == 5
    assert len(lines) == 5
    return RecursiveGrid(''.join(lines))

def test():
    example_data = '''
....#
#..#.
#..##
..#..
#....'''
    grid = parse_grid(example_data)
    iterate_until_seen_twice(grid)
    #grid.print_grid()
    assert grid.biodiversity_rating() == 2129920

    grid = parse_recursive_grid(example_data)
    for _ in range(10):
        grid.levels = grid.next_generation()
    #grid.print_grids()
    assert grid.total_bug_count() == 99

test()

def main():
    with open('input') as f:
        grid = parse_grid(f.read())
    iterate_until_seen_twice(grid)
    grid.print_grid()
    print(grid.biodiversity_rating())

#main()

def main2():
    with open('input') as f:
        grid = parse_recursive_grid(f.read())
    for _ in range(200):
        grid.levels = grid.next_generation()
    grid.print_grids()
    print(grid.total_bug_count())

main2()

