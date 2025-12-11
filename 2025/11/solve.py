from functools import cache

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

EXAMPLE2 = '''
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
'''

class Solver:
    def __init__(self, graph):
        self.graph = graph

    @cache
    def count_dac_fft_paths(self, node, dac, fft):
        if node == 'out':
            if dac and fft:
                return 1
            else:
                return 0
        r = 0
        for next in self.graph[node]:
            assert not (dac and next == 'dac')
            assert not (fft and next == 'fft')
            r += self.count_dac_fft_paths(next, dac or next == 'dac', fft or next == 'fft')
        return r

def solve2(s):
    solver = Solver(parse(s))
    return solver.count_dac_fft_paths('svr', False, False)

assert solve2(EXAMPLE2) == 2

with open('input') as f:
    s = f.read()

print(solve1(s))
print(solve2(s))
