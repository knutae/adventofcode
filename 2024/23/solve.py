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
                    result.add(tuple(sorted((a,b,c))))
    return result

assert len(sets_of_three(parse(EXAMPLE))) == 12

def solve1(data):
    graph = parse(data)
    sets = sets_of_three(graph)
    sets = [x for x in sets if any(v.startswith('t') for v in x)]
    return len(sets)

assert solve1(EXAMPLE) == 7

with open('input') as f:
    data = f.read()

print(solve1(data))
