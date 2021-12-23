from collections import defaultdict

EXAMPLE = '''
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
'''

PUZZLE_INPUT = '''
#############
#...........#
###B#B#D#D###
  #C#C#A#A#
  #########
'''

# The hashable state is represented as nested tuples: 4 types with 2 sorted positions, each a (x,y) tuple

def to_hashable_state(pods):
    return tuple(tuple(sorted(pods[c])) for c in 'ABCD')

def to_position_map(hashable_state):
    return {pod: set(positions) for pod, positions in zip('ABCD', hashable_state)}

def parse(data):
    pods = defaultdict(set)
    lines = data.strip().split('\n')
    assert lines[0] == '#############'
    assert lines[1] == '#...........#'
    for y, line in enumerate(lines[1:]):
        for x, c in enumerate(line[1:]):
            if c in 'ABCD':
                pods[c].add((x,y))
    return dict(pods)

def positions_between(pos1, pos2):
    if pos1[1] == 0:
        hallway, room = pos1, pos2
    else:
        hallway, room = pos2, pos1
    hx, hy = hallway
    rx, ry = room
    assert hy == 0
    assert ry in (1,2)
    # generate outer room position if needed
    if ry == 2:
        yield rx,1
    # generate hallway positions, except the position right outside the room (it's always empty anyway)
    for x in range(min(rx, hx)+1, max(rx, hx)):
        yield x,0

HALLWAY_POSITIONS = [(0,0),(1,0),(3,0),(5,0),(7,0),(9,0),(10,0)]
ENERGY_COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
TARGET_PODS = {
    'A': {(2,1),(2,2)},
    'B': {(4,1),(4,2)},
    'C': {(6,1),(6,2)},
    'D': {(8,1),(8,2)},
}

def valid_moves(pods):
    reverse_map = dict()
    for pod, positions in pods.items():
        for pos in positions:
            reverse_map[pos] = pod
    for pod, pod_positions in pods.items():
        pod_index = ord(pod) - ord('A')
        target_room_x = 2 + pod_index*2
        inner_room_position = (target_room_x, 2)
        outer_room_position = (target_room_x, 1)
        for source_pos in pod_positions:
            x, y = source_pos
            if y == 0:
                # in hallway: the only valid move is into the correct room
                if inner_room_position not in reverse_map:
                    target_pos = inner_room_position
                elif reverse_map[inner_room_position] == pod and outer_room_position not in reverse_map:
                    target_pos = outer_room_position
                else:
                    # the target room is not accessible
                    break
                if any(p in reverse_map for p in positions_between(source_pos, target_pos)):
                    # no path to target room
                    break
                # yay, found a valid move to the target room
                yield pod, source_pos, target_pos
            else:
                assert y in (1,2) # in a room
                if x == target_room_x and inner_room_position in pod_positions:
                    #print(f'No valid moves for {pod} at {source_pos}')
                    # already at correct room, no valid moves
                    continue
                for target_pos in HALLWAY_POSITIONS:
                    if target_pos in reverse_map:
                        continue
                    if any(p in reverse_map for p in positions_between(source_pos, target_pos)):
                        # no path to that hallway position
                        continue
                    # valid hallway move
                    yield pod, source_pos, target_pos

assert len(list(valid_moves(parse(EXAMPLE)))) == 28

def move_cost(pod, source_pos, target_pos):
    manhattan_distance = abs(source_pos[0] - target_pos[0]) + abs(source_pos[1] - target_pos[1])
    return manhattan_distance * ENERGY_COST[pod]

def search_step(prev_states, all_states, all_paths):
    next_states = set()
    for state in prev_states:
        assert state in all_states
        pods = to_position_map(state)
        for pod, source_pos, target_pos in valid_moves(pods):
            new_pods = {pod: set(positions) for pod, positions in pods.items()}
            new_pods[pod].remove(source_pos)
            new_pods[pod].add(target_pos)
            new_cost = all_states[state] + move_cost(pod, source_pos, target_pos)
            new_state = to_hashable_state(new_pods)
            if new_state in all_states and all_states[new_state] <= new_cost:
                continue
            #if new_state in next_states and next_states[new_state] <= new_cost:
            #    continue
            next_states.add(new_state)
            all_states[new_state] = new_cost
            all_paths[new_state] = state
    return next_states

def print_state(state):
    pods = to_position_map(state)
    reverse_map = dict()
    for pod, positions in pods.items():
        for pos in positions:
            reverse_map[pos] = pod
    def pod_at(x, y):
        return reverse_map.get((x,y),'.')
    print('\n#############')
    hallway = ''.join(pod_at(i,0) for i in range(11))
    print(f'#{hallway}#')
    print(f'###{pod_at(2,1)}#{pod_at(4,1)}#{pod_at(6,1)}#{pod_at(8,1)}###')
    print(f'  #{pod_at(2,2)}#{pod_at(4,2)}#{pod_at(6,2)}#{pod_at(8,2)}#')
    print('  #########\n')

def print_path(all_paths, state):
    if state in all_paths:
        print_path(all_paths, all_paths[state])
    print_state(state)

def solve1(data):
    pods = parse(data)
    #print_state(to_hashable_state(pods))
    all_states = {to_hashable_state(pods): 0}
    all_paths = dict()
    prev_states = set(all_states.keys())
    target_state = to_hashable_state(TARGET_PODS)
    while len(prev_states) > 0:
        next_states = search_step(prev_states, all_states, all_paths)
        #print(f'prev {len(prev_states)} next {len(next_states)} all {len(all_states)}')
        prev_states = next_states
    assert target_state in all_states
    #print_path(all_paths, target_state)
    return all_states[target_state]

assert solve1(EXAMPLE) == 12521
print(solve1(PUZZLE_INPUT))
