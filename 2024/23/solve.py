import collections

EXAMPLE = '''
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
'''

def parse(data):
    graph = collections.defaultdict(set)
    for line in data.strip().split('\n'):
        a, b = line.split('-')
        graph[a].add(b)
        graph[b].add(a)
    return dict(graph)

def sets_of_three(graph):
    result = set()
    for a, nodes in graph.items():
        for b in nodes:
            for c in graph[b]:
                if a in graph[c]:
                    result.add(frozenset((a,b,c)))
    return result

assert len(sets_of_three(parse(EXAMPLE))) == 12

def solve1(data):
    graph = parse(data)
    sets = sets_of_three(graph)
    sets = [x for x in sets if any(v.startswith('t') for v in x)]
    return len(sets)

assert solve1(EXAMPLE) == 7

def grow_network(graph, network):
    for candidate in graph:
        if candidate in network:
            continue
        if all(candidate in graph[node] for node in network):
            yield network | {candidate}

def solve2(data):
    graph = parse(data)
    networks = sets_of_three(graph)
    while True:
        new_networks = set()
        for network in networks:
            for new_network in grow_network(graph, network):
                new_networks.add(new_network)
        if len(new_networks) == 0:
            break
        networks = new_networks
    assert len(networks) == 1
    result = next(iter(networks))
    result = ','.join(sorted(result))
    return result

assert solve2(EXAMPLE) == 'co,de,ka,ta'

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
