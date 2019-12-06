import sys

def parse_input(s):
    graph = dict()
    for line in s.strip().split('\n'):
        [a, b] = line.split(')')
        assert b not in graph
        graph[b] = a
    return graph

def count_orbits(graph):
    count = 0
    for obj in graph:
        v = obj
        while v in graph:
            count += 1
            v = graph[v]
        assert v == 'COM'
    return count

def orbit_path(graph, obj):
    assert obj in graph
    path = []
    while obj in graph:
        obj = graph[obj]
        path.append(obj)
    assert path[-1] == 'COM'
    return path

def shortest_transfer(graph, obj1, obj2):
    path1 = orbit_path(graph, obj1)
    path2 = orbit_path(graph, obj2)
    for i, a in enumerate(path1):
        for j, b in enumerate(path2):
            if a == b:
                return i + j
    assert False

def test():
    test_input = '''
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
'''
    assert count_orbits(parse_input(test_input)) == 42
    test2_input = test_input + 'K)YOU\nI)SAN'
    graph = parse_input(test2_input)
    assert orbit_path(graph, 'YOU') == ['K', 'J', 'E', 'D', 'C', 'B', 'COM']
    assert orbit_path(graph, 'SAN') == ['I', 'D', 'C', 'B', 'COM']
    assert shortest_transfer(graph, 'YOU', 'SAN') == 4

test()
#print(count_orbits(parse_input(sys.stdin.read())))
print(shortest_transfer(parse_input(sys.stdin.read()), 'YOU', 'SAN'))
