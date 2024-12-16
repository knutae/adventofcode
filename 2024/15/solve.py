from typing import NamedTuple

SMALL_EXAMPLE = '''
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
'''

EXAMPLE = '''
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
'''

BIG_BOX_EXAMPLE = '''
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
'''

DIRECTIONS = {
    '<': (-1, 0),
    '>': (1, 0),
    '^': (0, -1),
    'v': (0, 1),
}

class Warehouse:
    def __init__(self, walls, boxes, robot):
        self.walls = frozenset(walls)
        self.boxes = list(boxes)
        self.robot = robot

    def move_box(self, pos, direction):
        index = self.boxes.index(pos)
        x, y = pos
        dx, dy = direction
        new_pos = x+dx, y+dy
        if new_pos in self.walls:
            return False
        if new_pos in self.boxes and not self.move_box(new_pos, direction):
            return False
        self.boxes[index] = new_pos
        return True

    def move_robot(self, direction):
        x, y = self.robot
        dx, dy = direction
        new_pos = x+dx, y+dy
        if new_pos in self.walls:
            return False
        if new_pos in self.boxes and not self.move_box(new_pos, direction):
            return False
        self.robot = new_pos
        return True

def left_pos(pos):
    x, y = pos
    return x-1, y

def right_pos(pos):
    x, y = pos
    return x+1, y

class BigBoxWarehouse:
    def __init__(self, walls, boxes, robot):
        self.walls = frozenset(walls)
        self.boxes = list(boxes)
        self.robot = robot

    def move_box(self, pos, direction, dry_run):
        index = self.boxes.index(pos)
        x, y = pos
        dx, dy = direction
        new_pos = x+dx, y+dy
        if new_pos in self.walls or right_pos(new_pos) in self.walls:
            return False
        pushed_boxes = []
        if dx == -1 and left_pos(new_pos) in self.boxes:
            pushed_boxes.append(left_pos(new_pos))
        if dx == 1 and right_pos(new_pos) in self.boxes:
            pushed_boxes.append(right_pos(new_pos))
        if dx == 0:
            # push up/down, check for up to two boxes at three locations
            for nx in (x-1, x, x+1):
                np = (nx,y+dy)
                if np in self.boxes:
                    pushed_boxes.append(np)
            assert len(pushed_boxes) <= 2
        if not all(self.move_box(p, direction, dry_run) for p in pushed_boxes):
            return False
        if not dry_run:
            self.boxes[index] = new_pos
        return True

    def move_robot(self, direction):
        #print(direction)
        x, y = self.robot
        dx, dy = direction
        new_pos = x+dx, y+dy
        if new_pos in self.walls:
            return False
        if new_pos in self.boxes and not self.move_box(new_pos, direction, True):
            return False
        if left_pos(new_pos) in self.boxes and not self.move_box(left_pos(new_pos), direction, True):
            return False
        if new_pos in self.boxes:
            assert self.move_box(new_pos, direction, False)
        if left_pos(new_pos) in self.boxes:
            assert self.move_box(left_pos(new_pos), direction, False)
        self.robot = new_pos
        return True

    def print(self):
        def char_at(x,y):
            if (x,y) in self.walls:
                return '#'
            if (x,y) in self.boxes:
                return '['
            if (x-1,y) in self.boxes:
                return ']'
            if (x,y) == self.robot:
                return '@'
            return '.'

        width = max(x for x,_ in self.walls) + 1
        height = max(y for _,y in self.walls) + 1
        print('\n'.join(
            ''.join(char_at(x, y) for x in range(width))
            for y in range(height)))

def parse(data, widened=False):
    warehouse, moves = data.strip().split('\n\n')
    walls = set()
    boxes = set()
    robot = None
    for y, line in enumerate(warehouse.split('\n')):
        if widened:
            line = line.replace('#', '##').replace('.', '..').replace('O', 'O.').replace('@', '@.')
        for x, c in enumerate(line):
            pos = x, y
            if c == '#':
                walls.add(pos)
            elif c == 'O':
                boxes.add(pos)
            elif c == '@':
                assert robot is None
                robot = pos
            else:
                assert c == '.'
    if widened:
        warehouse = BigBoxWarehouse(walls, boxes, robot)
    else:
        warehouse = Warehouse(walls, boxes, robot)
    return warehouse, [DIRECTIONS[c] for c in moves.replace('\n', '')]

def solve1(data):
    warehouse, directions = parse(data)
    for direction in directions:
        warehouse.move_robot(direction)
    return sum(x + y*100 for x, y in warehouse.boxes)

def solve2(data):
    warehouse, directions = parse(data, True)
    for direction in directions:
        warehouse.move_robot(direction)
    #warehouse.print()
    return sum(x + y*100 for x, y in warehouse.boxes)

assert solve1(SMALL_EXAMPLE) == 2028
assert solve1(EXAMPLE) == 10092
solve2(BIG_BOX_EXAMPLE)
assert solve2(EXAMPLE) == 9021

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
