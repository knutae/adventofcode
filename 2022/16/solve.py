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
    added_pressure: int

def generate_transitions(valves, state: State, total_pressure):
    current_pressure = state.current_pressure + state.added_pressure
    new_total_pressure = total_pressure + current_pressure
    if len(state.closed_valves) == 0:
        # nothing to do after all valves are open
        # use an empty location to improve hashing
        yield State(
            '',
            state.closed_valves,
            current_pressure,
            0), new_total_pressure
        return
    if state.pos in state.closed_valves:
        # open the current valve
        yield State(
            state.pos,
            frozenset.difference(state.closed_valves, {state.pos}),
            current_pressure,
            valves[state.pos][0]), new_total_pressure
    for tunnel in valves[state.pos][1]:
        # move to a different location
        yield State(
            tunnel,
            state.closed_valves,
            current_pressure,
            0), new_total_pressure

def solve1(input, verbose=False):
    valves = parse(input)
    closed_valves ={v for v in valves if valves[v][0] > 0}
    states = {State('AA', frozenset(closed_valves), 0, 0): 0}
    for minute in range(30):
        new_states = dict()
        for s, total_pressure in states.items():
            for ns, new_total_pressure in generate_transitions(valves, s, total_pressure):
                if ns not in new_states or new_states[ns] < new_total_pressure:
                    new_states[ns] = new_total_pressure
        states = new_states
        if verbose:
            print(minute, len(states))
    return max(states.values())

assert solve1(EXAMPLE) == 1651

with open('input') as f:
    input = f.read()

print(solve1(input))
