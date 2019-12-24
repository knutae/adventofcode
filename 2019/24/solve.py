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

test()

def main():
    with open('input') as f:
        grid = parse_grid(f.read())
    iterate_until_seen_twice(grid)
    grid.print_grid()
    print(grid.biodiversity_rating())

main()