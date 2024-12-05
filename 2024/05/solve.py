EXAMPLE = '''
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
'''

def parse(data):
    ordering, updates = data.strip().split('\n\n')
    order_set = set()
    update_list = []
    for line in ordering.split('\n'):
        order_set.add(tuple(int(x) for x in line.split('|')))
    for line in updates.split('\n'):
        update_list.append([int(x) for x in line.split(',')])
    return order_set, update_list

def is_topologically_sorted(update, order_set):
    for i, a in enumerate(update):
        for b in update[i+1:]:
            if (b, a) in order_set:
                return False
    return True

def solve1(data):
    order_set, updates = parse(data)
    r = 0
    for update in updates:
        if is_topologically_sorted(update, order_set):
            r += update[len(update) // 2]
    return r

assert solve1(EXAMPLE) == 143

with open('input') as f:
    data = f.read()

print(solve1(data))
