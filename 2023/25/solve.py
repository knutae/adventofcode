import collections
import itertools

EXAMPLE = '''
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
'''

def parse(data):
    lines = data.strip().split('\n')
    graph = collections.defaultdict(set)
    for line in lines:
        lhs, *rhs = line.split()
        assert lhs[-1] == ':'
        lhs = lhs[:-1]
        for r in rhs:
            graph[lhs].add(r)
            graph[r].add(lhs)
    return graph

def remove_node(graph, node):
    if node not in graph:
        return
    connected = graph[node]
    del graph[node]
    for r in connected:
        r_connected = graph[r]
        assert node in r_connected
        r_connected.remove(node)
        if len(r_connected) == 0:
            del graph[r]

def remove_link(graph, a, b):
    a_connected = graph[a]
    b_connected = graph[b]
    assert b in a_connected
    assert a in b_connected
    a_connected.remove(b)
    b_connected.remove(a)

def deep_copy(graph):
    return {k: set(v) for k, v in graph.items()}

def split(graph):
    distinct_nodes = []
    remaining = deep_copy(graph)
    while remaining:
        node = next(iter(remaining.keys()))
        nodes = {node}
        seen = {node}
        while nodes:
            next_nodes = set()
            for node in nodes:
                for r in remaining.get(node, set()):
                    if r not in seen:
                        seen.add(r)
                        next_nodes.add(r)
            nodes = next_nodes
        distinct_nodes.append(seen)
        for node in seen:
            remove_node(remaining, node)
    return distinct_nodes

def generate_graphviz(graph):
    ignore_reverse = set()
    lines = ['strict graph {']
    for key, values in graph.items():
        for value in values:
            if (value, key) not in ignore_reverse:
                ignore_reverse.add((key, value))
                lines.append(f'    {key} -- {value}')
    lines.append('}')
    return '\n'.join(lines)

def loop_length(graph, a, b):
    graph = deep_copy(graph)
    remove_link(graph, a, b)
    nodes = [a]
    seen = {a}
    length = 1
    while b not in seen:
        assert len(nodes) > 0
        new_nodes = []
        for node in nodes:
            for v in graph[node]:
                if v not in seen:
                    seen.add(v)
                    new_nodes.append(v)
        nodes = new_nodes
        length += 1
    return length

def solve1(data):
    graph = parse(data)
    #print(generate_graphviz(graph))
    nodes = list(sorted(graph.keys()))
    links = [(a,b) for a, b in itertools.combinations(nodes, 2) if b in graph[a]]
    links.sort(key=lambda link: loop_length(graph, *link), reverse=True)
    solution = None
    for x, y, z in itertools.combinations(links, 3):
        tmp_graph = deep_copy(graph)
        remove_link(tmp_graph, *x)
        remove_link(tmp_graph, *y)
        remove_link(tmp_graph, *z)
        groups = split(tmp_graph)
        if len(groups) == 2:
            #print(x, y, z)
            solution = groups
            break
    #print(solution)
    a, b = solution
    return len(a) * len(b)

assert solve1(EXAMPLE) == 54

with open('input') as f:
    data = f.read()

print(solve1(data))
