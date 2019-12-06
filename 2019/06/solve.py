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

test()
print(count_orbits(parse_input(sys.stdin.read())))
