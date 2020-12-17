EXAMPLE = '''
.#.
..#
###'''

def parse(input):
    lines = input.strip().split('\n')
    cells = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                cells.add((x,y,0))
    return cells

def cells_range(cells):
    x,y,z = next(iter(cells))
    rx = range(x,x+1)
    ry = range(y,y+1)
    rz = range(z,z+1)
    for x,y,z in cells:
        rx = range(min(x, rx.start), max(x+1, rx.stop))
        ry = range(min(y, ry.start), max(y+1, ry.stop))
        rz = range(min(z, rz.start), max(z+1, rz.stop))
    return rx, ry, rz

def expand_range(r):
    return range(r.start-1, r.stop+1)

def expanded_cells_range(cells):
    return tuple(map(lambda r: range(r.start-1, r.stop+1), cells_range(cells)))

def cells_print(cells):
    rx, ry, rz = cells_range(cells)
    for z in rz:
        print(f'z={z}')
        for y in ry:
            print(''.join('#' if (x,y,z) in cells else '.' for x in rx))
        print('')

def count_neighbors(cells, cell, limit=4):
    px,py,pz = cell
    count = 0
    for x in (px-1, px, px+1):
        for y in (py-1, py, py+1):
            for z in (pz-1, pz, pz+1):
                neighbor = x,y,z
                if neighbor != cell and neighbor in cells:
                    count += 1
                    if count >= limit:
                        return count
    return count

def step(cells):
    new_cells = set()
    rx, ry, rz = expanded_cells_range(cells)
    for x in rx:
        for y in ry:
            for z in rz:
                cell = x,y,z
                count = count_neighbors(cells, cell)
                if cell in cells:
                    # remain active if count is 2 or 3
                    if count == 2 or count == 3:
                        new_cells.add(cell)
                else:
                    # become active if count is 3
                    if count == 3:
                        new_cells.add(cell)
    return new_cells

def solve1(input, cycles=6):
    cells = parse(input)
    #cells_print(cells)
    for cycle in range(cycles):
        cells = step(cells)
        #print(f'\nCycle {cycle+1}\n')
        #cells_print(cells)
    return len(cells)

assert solve1(EXAMPLE) == 112

with open('input') as f:
    input = f.read()
print(solve1(input))
