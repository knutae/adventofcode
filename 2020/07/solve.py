EXAMPLE = '''
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
'''

EXAMPLE2 = '''
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
'''

def parse_n_bags(s):
    words = s.split(' ')
    assert len(words) == 4
    bag = ' '.join(words[1:3])
    count = int(words[0])
    if count == 1:
        assert words[3] == 'bag'
    else:
        assert words[3] == 'bags'
    return bag, count

def parse_line(line):
    assert line.endswith('.')
    line = line[:-1]
    [bag, rest] = line.split(' bags contain ')
    if rest == 'no other bags':
        contents = {}
    else:
        contents = dict(parse_n_bags(x) for x in rest.split(', '))
    return bag, contents

def parse(input):
    lines = map(parse_line, input.strip().split('\n'))
    return {bag: contents for bag, contents in lines}

def can_contain_shiny_gold(bag, bag_map):
    contents = bag_map[bag]
    if len(contents) == 0:
        return False
    if 'shiny gold' in contents:
        return True
    for key in contents:
        if can_contain_shiny_gold(key, bag_map):
            return True
    return False

def solve1(bag_map):
    return sum(1 for bag in bag_map if can_contain_shiny_gold(bag, bag_map))

def count_total_bags(bag, bag_map, cache):
    if bag in cache:
        return cache[bag]
    total = 1 # self
    contents = bag_map[bag]
    for content_bag, count in contents.items():
        total += count * count_total_bags(content_bag, bag_map, cache)
    cache[bag] = total
    return total

def solve2(bag_map):
    return count_total_bags('shiny gold', bag_map, dict()) - 1

bag_map = parse(EXAMPLE)
#print(bag_map)
assert solve1(bag_map) == 4
assert solve2(bag_map) == 32
assert solve2(parse(EXAMPLE2)) == 126

with open('input') as f:
    bag_map = parse(f.read())
print(solve1(bag_map))
print(solve2(bag_map))
