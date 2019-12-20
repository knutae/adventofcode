import sys
import typing

class Position(typing.NamedTuple):
    x: int
    y: int

class PortalLocation(typing.NamedTuple):
    door: Position
    floor: Position

class Portal(typing.NamedTuple):
    name: str
    locations: typing.List[PortalLocation]

PORTAL_LETTERS = range(ord('A'),ord('Z')+1)

def has_portal_letter(tiles, x, y):
    return Position(x,y) in tiles and ord(tiles[(x,y)]) in PORTAL_LETTERS

def adjacent_floor(tiles, x, y):
    for dx, dy in [(0,-1), (0,1),(-1,0),(1,0)]:
        pos = Position(x+dx, y+dy)
        if pos in tiles and tiles[pos] == '.':
            return pos
    return None

def is_portal(tiles, x, y):
    if not has_portal_letter(tiles, x, y):
        return False
    return adjacent_floor(tiles, x, y) is not None

def portal_name(tiles, x, y):
    assert has_portal_letter(tiles, x, y)
    for dx, dy in [(0,-1), (0,1),(-1,0),(1,0)]:
        if has_portal_letter(tiles, x+dx, y+dy):
            return tiles[(min(x,x+dx),min(y,y+dy))] + tiles[(max(x,x+dx),max(y,y+dy))]
    assert False

def portal_location(tiles, x, y):
    assert is_portal(tiles, x, y)
    return PortalLocation(door=Position(x, y), floor=adjacent_floor(tiles, x, y))

class Dungeon:
    def __init__(self, tiles, width, height, portals):
        self.tiles = tiles
        self.width = width
        self.height = height
        self.portals = portals
        self.start_pos = portals['AA'].locations[0].floor
        self.target_pos = portals['ZZ'].locations[0].floor

def parse(s):
    s = s.strip('\n')
    #grid = []
    tiles = dict()
    lines = s.split('\n')
    height = len(lines)
    width = max(len(line) for line in lines)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            tiles[Position(x,y)] = c
    #print(tiles)
    #print(width, height)
    portals = dict()
    for x in range(width):
        for y in range(height):
            if is_portal(tiles, x, y):
                name = portal_name(tiles, x, y)
                #print(f'portal at {x},{y}: {name}')
                if name in portals:
                    portal = portals[name]
                else:
                    portal = Portal(name=name, locations=list())
                    portals[name] = portal
                portal.locations.append(portal_location(tiles, x, y))
                tiles[Position(x,y)] = portal
    #print(portals)
    #print(portals['AA'])
    for portal in portals.values():
        if portal.name in ['AA','ZZ']:
            assert len(portal.locations) == 1
        else:
            assert len(portal.locations) == 2
    return Dungeon(tiles, width, height, portals)

def enumerate_moves(d: Dungeon, pos: Position):
    x, y = pos
    for dx, dy in ((0,-1),(-1,0),(1,0),(0,1)):
        candidate = Position(x+dx, y+dy)
        what = d.tiles[candidate]
        if what == '.':
            yield candidate
        elif isinstance(what, Portal):
            for loc in what.locations:
                if loc.floor != candidate:
                    yield loc.floor

def solve(d: Dungeon):
    visited = {d.start_pos}
    current_positions = [d.start_pos]
    steps = 0
    while True:
        steps += 1
        new_positions = list()
        for pos in current_positions:
            for new_pos in enumerate_moves(d, pos):
                if new_pos == d.target_pos:
                    #print(steps)
                    return steps
                if new_pos not in visited:
                    visited.add(new_pos)
                    new_positions.append(new_pos)
        current_positions = new_positions

def test():
    small_example = '''
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       '''
    d = parse(small_example)
    assert d.start_pos == Position(9,2)
    assert d.target_pos == Position(13,16)
    assert solve(d) == 23
    large_example = '''
                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               '''
    d = parse(large_example)
    assert solve(d) == 58

test()

def main():
    with open('input') as f:
        d = parse(f.read())
    print(solve(d))

main()
