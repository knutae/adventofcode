EXAMPLE = '''
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
'''

def parse(s):
    def parse_line(line):
        device, outputs = line.split(': ')
        outputs = outputs.split(' ')
        return device, outputs
    
    return dict(parse_line(line) for line in s.strip().split('\n'))

def count_paths_to_out(graph, node):
    if node == 'out':
        return 1
    r = 0
    for next in graph[node]:
        r += count_paths_to_out(graph, next)
    return r

def solve1(s):
    graph = parse(s)
    return count_paths_to_out(graph, 'you')

assert solve1(EXAMPLE) == 5

with open('input') as f:
    s = f.read()

print(solve1(s))
