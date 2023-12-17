EXAMPLE = '''
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
'''

def parse(data):
    lines = data.strip().split('\n')
    return [[int(c) for c in line] for line in lines]

def within_grid(dimensions, pos):
    w, h = dimensions
    x, y = pos
    return x >= 0 and x < w and y >= 0 and y < h

def move(pos, dir, amount=1):
    x,y = pos
    dx,dy = dir
    return x+dx*amount, y+dy*amount

def valid_moves(dimensions, pos, dir, straight_count):
    # move straight
    if straight_count < 3:
        new_pos = move(pos, dir)
        if within_grid(dimensions, new_pos):
            yield new_pos, dir, straight_count + 1
    # turn left/right
    turn_directions = [(0,-1),(0,1)] if dir[1] == 0 else [(-1,0),(1,0)]
    for turn_dir in turn_directions:
        new_pos = move(pos, turn_dir)
        if within_grid(dimensions, new_pos):
            yield new_pos, turn_dir, 1

def solve1(data):
    grid = parse(data)
    dimensions = w,h = len(grid[0]), len(grid)
    # key: tuple(pos,dir,straight_count)
    start_keys = [((0,0),(0,1),0), ((0,0),(1,0),0)]
    heat_loss = {k: 0 for k in start_keys}
    keys = list(start_keys)
    while keys:
        new_keys = []
        for key in keys:
            prev_heat_loss = heat_loss[key]
            pos, dir, count = key
            for new_key in valid_moves(dimensions, pos, dir, count):
                new_pos, _, _ = new_key
                x,y = new_pos
                new_heat_loss = prev_heat_loss + grid[y][x]
                if new_key not in heat_loss or new_heat_loss < heat_loss[new_key]:
                    heat_loss[new_key] = new_heat_loss
                    new_keys.append(new_key)
        keys = new_keys
        #print(keys)
    target_pos = (w-1), (h-1)
    candidates = [val for key,val in heat_loss.items() if key[0] == target_pos]
    #print(candidates)
    return min(candidates)

assert solve1(EXAMPLE) == 102

def valid_moves2(dimensions, pos, dir, straight_count):
    # move straight
    if straight_count < 10:
        new_pos = move(pos, dir)
        if within_grid(dimensions, new_pos):
            yield new_pos, dir, straight_count + 1
    if straight_count < 4:
        # too early to turn
        return
    # turn left/right
    turn_directions = [(0,-1),(0,1)] if dir[1] == 0 else [(-1,0),(1,0)]
    for turn_dir in turn_directions:
        if not within_grid(dimensions, move(pos, turn_dir, 4)):
            # no point in turning if 4 moves lands us outside the grid
            continue
        new_pos = move(pos, turn_dir)
        if within_grid(dimensions, new_pos):
            yield new_pos, turn_dir, 1

def solve2(data):
    grid = parse(data)
    dimensions = w,h = len(grid[0]), len(grid)
    # key: tuple(pos,dir,straight_count)
    start_keys = [((0,0),(0,1),0), ((0,0),(1,0),0)]
    heat_loss = {k: 0 for k in start_keys}
    keys = list(start_keys)
    while keys:
        new_keys = []
        for key in keys:
            prev_heat_loss = heat_loss[key]
            pos, dir, count = key
            for new_key in valid_moves2(dimensions, pos, dir, count):
                new_pos, _, _ = new_key
                x,y = new_pos
                new_heat_loss = prev_heat_loss + grid[y][x]
                if new_key not in heat_loss or new_heat_loss < heat_loss[new_key]:
                    heat_loss[new_key] = new_heat_loss
                    new_keys.append(new_key)
        keys = new_keys
        #print(keys)
    target_pos = (w-1), (h-1)
    candidates = [val for key,val in heat_loss.items() if key[0] == target_pos and key[2] >= 4]
    return min(candidates)

assert solve1(EXAMPLE) == 102
assert solve2(EXAMPLE) == 94

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
