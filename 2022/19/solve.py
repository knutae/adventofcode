from collections import defaultdict

EXAMPLE = '''
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
'''

def parse_robot(input):
    [_, resource, _, _, cost] = input.split(maxsplit=4)
    cost = [c.split() for c in cost.split(' and ')]
    cost = {b: int(a) for a, b in cost}
    return resource, cost

def parse_blueprint(line):
    line = line.rstrip('.')
    [number, robots] = line.split(': ')
    [_, number] = number.split()
    robots = dict(parse_robot(r) for r in robots.split('. ') if r)
    return int(number), robots

def parse(input):
    return dict(parse_blueprint(line) for line in input.strip().split('\n'))

RESOURCE_INDEX = ['ore', 'clay', 'obsidian', 'geode']

def transitions(blueprint, robots, resources):
    # not building a robot is always an option
    total_resources = tuple(a+b for a,b in zip(robots, resources))
    yield robots, total_resources
    for robot, costs in blueprint.items():
        if all(cost <= resource for cost, resource in zip(costs, resources)):
            # enough resources to build this robot
            new_robots = tuple(count + int(robot == i) for i, count in enumerate(robots))
            new_resources = tuple(r - cost for r, cost in zip(total_resources, costs))
            yield new_robots, new_resources

def all_counts_higher(a, b):
    return a != b and all(x >= y for x, y in zip(a, b))

def simulate(blueprint, steps, verbose=False):
    blueprint = {
        RESOURCE_INDEX.index(robot): tuple(costs.get(RESOURCE_INDEX[i], 0) for i in range(4))
        for robot, costs in blueprint.items()
    }
    current_states = {(0,0,0,0): {(1,0,0,0)}}
    for step in range(steps):
        new_states = defaultdict(set)
        for resources, all_robots in current_states.items():
            for robots in list(all_robots):
                for new_robots, new_resources in transitions(blueprint, robots, resources):
                    new_states[new_resources].add(new_robots)
        if verbose: print(step, sum(len(r) for r in new_states.values()))
        if step < steps - 1:
            for resources, all_robots in new_states.items():
                for robots in list(all_robots):
                    if any(
                        all_counts_higher(other_robots, robots)
                        for other_robots in all_robots):
                        all_robots.remove(robots)
            if verbose: print(step, sum(len(r) for r in new_states.values()))
        current_states = {k:set(v) for k,v in new_states.items() if len(v)>0}
    return max(geode for _,_,_,geode in current_states)

def solve1(input, verbose=False):
    result = 0
    for num, blueprint in parse(input).items():
        geodes = simulate(blueprint, 24, verbose=verbose)
        #print("***", num, geodes)
        result += num * geodes
    return result

assert solve1(EXAMPLE) == 33

with open('input') as f:
    input = f.read()

print(solve1(input))
