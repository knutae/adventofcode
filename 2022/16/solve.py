from dataclasses import dataclass
import typing

EXAMPLE = '''
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''

def parse_valve(line):
    [first, second] = line.split('; ')
    [_, valve, _, _, rate] = first.split()
    [_, _, _, _, tunnels] = second.split(maxsplit=4)
    rate = int(rate.split('=')[1])
    tunnels = tunnels.split(', ')
    return valve, rate, tunnels

def parse(input):
    valves = [parse_valve(line) for line in input.strip().split('\n')]
    return {valve[0]: (valve[1], valve[2]) for valve in valves}

#print(parse(EXAMPLE))

@dataclass(frozen=True)
class State:
    pos: str
    closed_valves: typing.FrozenSet[str]
    current_pressure: int
    total_pressure: int
    added_pressure: int

def generate_transitions(valves, state: State):
    current_pressure = state.current_pressure + state.added_pressure
    total_pressure = state.total_pressure + current_pressure
    if len(state.closed_valves) == 0:
        # nothing to do after all valves are open
        # use an empty location to improve hashing
        yield State(
            '',
            state.closed_valves,
            current_pressure,
            total_pressure,
            0)
        return
    if state.pos in state.closed_valves:
        # open the current valve
        yield State(
            state.pos,
            frozenset.difference(state.closed_valves, {state.pos}),
            current_pressure,
            total_pressure,
            valves[state.pos][0])
    for tunnel in valves[state.pos][1]:
        # move to a different location
        yield State(
            tunnel,
            state.closed_valves,
            current_pressure,
            total_pressure,
            0)

def solve1(input, verbose=False):
    valves = parse(input)
    closed_valves ={v for v in valves if valves[v][0] > 0}
    states = {State('AA', frozenset(closed_valves), 0, 0, 0)}
    for minute in range(30):
        new_states = set()
        for s in states:
            for ns in generate_transitions(valves, s):
                new_states.add(ns)
        states = new_states
        if verbose:
            print(minute, len(states))
    return max(s.total_pressure for s in states)

assert solve1(EXAMPLE) == 1651

with open('input') as f:
    input = f.read()

print(solve1(input))
