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

def parse(data):
    warehouse, moves = data.strip().split('\n\n')
    walls = set()
    boxes = set()
    robot = None
    for y, line in enumerate(warehouse.split('\n')):
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
    return Warehouse(walls, boxes, robot), [DIRECTIONS[c] for c in moves.replace('\n', '')]

def solve1(data):
    warehouse, directions = parse(data)
    for direction in directions:
        warehouse.move_robot(direction)
    return sum(x + y*100 for x, y in warehouse.boxes)

assert solve1(SMALL_EXAMPLE) == 2028
assert solve1(EXAMPLE) == 10092

with open('input') as f:
    data = f.read()

print(solve1(data))
