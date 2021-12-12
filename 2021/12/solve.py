from collections import defaultdict

EXAMPLE1='''
start-A
start-b
A-c
A-b
b-d
A-end
b-end
'''

EXAMPLE2='''
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
'''

EXAMPLE3='''
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
'''

def parse(data):
    caves = defaultdict(set)
    for line in data.strip().split('\n'):
        a,b = line.split('-')
        caves[a].add(b)
        caves[b].add(a)
    return caves

def generate_paths(graph, prefix):
    if prefix[-1] == 'end':
        # yield complete path and quit
        yield prefix
        return
    for node in graph[prefix[-1]]:
        if node.islower() and node in prefix:
            # prevent multiple visits of small caves, including 'start'
            continue
        for path in generate_paths(graph, prefix + (node,)):
            yield path

def solve1(graph):
    return sum(1 for _ in generate_paths(graph, ('start',)))

def generate_paths2(graph, prefix):
    if prefix[-1] == 'end':
        # yield complete path and quit
        yield prefix
        return
    visited_twice = any(x.islower() and prefix.count(x) == 2 for x in prefix)
    for node in graph[prefix[-1]]:
        if node == 'start':
            continue
        if visited_twice and (node.islower() and node in prefix):
            # after visiting a single node twice, prevent any more double visits
            continue
        for path in generate_paths2(graph, prefix + (node,)):
            yield path

def solve2(graph):
    prefix = ('start',)
    return(sum(1 for _ in generate_paths2(graph, prefix)))

assert solve1(parse(EXAMPLE1)) == 10
assert solve1(parse(EXAMPLE2)) == 19
assert solve1(parse(EXAMPLE3)) == 226

assert solve2(parse(EXAMPLE1)) == 36
assert solve2(parse(EXAMPLE2)) == 103
assert solve2(parse(EXAMPLE3)) == 3509

with open('input') as f:
    graph = parse(f.read())

print(solve1(graph))
print(solve2(graph))
