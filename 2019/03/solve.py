
def calculate_points(path):
    points = set()
    pos = (0,0)
    for move in path.split(','):
        d = move[0]
        n = int(move[1:])
        if d == 'R':
            inc = (1,0)
        elif d == 'L':
            inc = (-1,0)
        elif d == 'U':
            inc = (0,1)
        elif d == 'D':
            inc = (0,-1)
        else:
            assert False
        for _ in range(n):
            pos = (pos[0]+inc[0], pos[1]+inc[1])
            points.add(pos)
    return points

def solve(path1, path2):
    p1 = calculate_points(path1)
    p2 = calculate_points(path2)
    intersections = p1 & p2
    #print(intersections)
    shortest = min(abs(a)+abs(b) for (a,b) in intersections)
    #print(shortest)
    return shortest

assert solve('R8,U5,L5,D3', 'U7,R6,D4,L4') == 6
assert solve('R75,D30,R83,U83,L12,D49,R71,U7,L72','U62,R66,U55,R34,D71,R55,D58,R83') == 159
assert solve('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7') == 135

path1 = input()
path2 = input()
print(solve(path1, path2))
