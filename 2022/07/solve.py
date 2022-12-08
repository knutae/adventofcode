import os.path
from collections import defaultdict

TEST_INPUT = '''
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''

def parse(input):
    cwd = None
    dirs = defaultdict(list)
    for line in input.strip().split('\n'):
        words = line.split()
        if words[0] == '$':
            if words[1] == 'cd':
                assert len(words) == 3
                if words[2] == '/':
                    cwd = '/'
                elif words[2] == '..':
                    cwd = os.path.split(cwd)[0]
                else:
                    cwd = os.path.join(cwd, words[2])
            else:
                assert words[1] == 'ls' and len(words) == 2
        else:
            [prefix, name] = words
            if prefix == 'dir':
                dirs[cwd].append((name, os.path.join(cwd, name)))
            else:
                size = int(prefix)
                dirs[cwd].append((name, size))
    return dirs

def calculate_sizes(dirs):
    sizes = dict()
    def calculate_size(dir):
        if dir in sizes:
            return sizes[dir]
        size = 0
        for _, entry in dirs[dir]:
            if isinstance(entry, int):
                size += entry
            else:
                size += calculate_size(entry)
        sizes[dir] = size
        return size
    calculate_size('/')
    return sizes


def solve1(input):
    dirs = parse(input)
    sizes = calculate_sizes(dirs)
    return sum(size for size in sizes.values() if size <= 100000)

def solve2(input):
    dirs = parse(input)
    sizes = calculate_sizes(dirs)
    used_size = sizes['/']
    return min(size for size in sizes.values() if used_size - size <= 40000000)

assert solve1(TEST_INPUT) == 95437
assert solve2(TEST_INPUT) == 24933642

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
