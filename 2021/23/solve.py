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
    assert ry > 0
    # generate room positions
    for y in range(1, ry):
        yield rx,y
    # generate hallway positions, except the position right outside the room (it's always empty anyway)
    for x in range(min(rx, hx)+1, max(rx, hx)):
        yield x,0

HALLWAY_POSITIONS = [(0,0),(1,0),(3,0),(5,0),(7,0),(9,0),(10,0)]
ENERGY_COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

def target_pods(room_depth):
    pods = dict()
    for pod, x in zip('ABCD', (2,4,6,8)):
        pods[pod] = {(x,y) for y in range(1, room_depth+1)}
    return pods

def valid_moves(pods, room_depth):
    reverse_map = dict()
    for pod, positions in pods.items():
        for pos in positions:
            reverse_map[pos] = pod
    room_y_range = range(1, room_depth+1)
    for pod, pod_positions in pods.items():
        pod_index = ord(pod) - ord('A')
        target_room_x = 2 + pod_index*2
        target_room_is_ready = all(reverse_map.get((target_room_x, y), pod) == pod for y in room_y_range)
        for source_pos in pod_positions:
            x, y = source_pos
            if y == 0:
                # in hallway: the only valid move is into the correct room
                if not target_room_is_ready:
                    # the target room is not accessible
                    continue
                target_pos = max((target_room_x, target_y) for target_y in room_y_range if (target_room_x, target_y) not in reverse_map)
                if any(p in reverse_map for p in positions_between(source_pos, target_pos)):
                    # no path to target room
                    continue
                # yay, found a valid move to the target room
                yield pod, source_pos, target_pos
            else:
                assert y > 0 # in a room
                if x == target_room_x and target_room_is_ready:
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

assert len(list(valid_moves(parse(EXAMPLE), 2))) == 28

def move_cost(pod, source_pos, target_pos):
    manhattan_distance = abs(source_pos[0] - target_pos[0]) + abs(source_pos[1] - target_pos[1])
    return manhattan_distance * ENERGY_COST[pod]

def search_step(prev_states, all_states, all_paths, room_depth):
    next_states = set()
    for state in prev_states:
        assert state in all_states
        pods = to_position_map(state)
        for pod, source_pos, target_pos in valid_moves(pods, room_depth):
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

def print_state(state, room_depth):
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
    for y in range(1, room_depth+1):
        pad = '##' if y == 1 else '  '
        print(f'{pad}#{pod_at(2,y)}#{pod_at(4,y)}#{pod_at(6,y)}#{pod_at(8,y)}#{pad}')
    print('  #########\n')

def print_path(all_paths, state, room_depth):
    if state in all_paths:
        print_path(all_paths, all_paths[state], room_depth)
    print_state(state, room_depth)

def solve(pods, room_depth, verbose=False):
    #print_state(to_hashable_state(pods))
    all_states = {to_hashable_state(pods): 0}
    all_paths = dict()
    prev_states = set(all_states.keys())
    target_state = to_hashable_state(target_pods(room_depth))
    if verbose:
        print_state(to_hashable_state(pods), room_depth)
        print_state(target_state, room_depth)
    while len(prev_states) > 0:
        next_states = search_step(prev_states, all_states, all_paths, room_depth)
        if verbose:
            print(f'prev {len(prev_states)} next {len(next_states)} all {len(all_states)}')
        prev_states = next_states
    assert target_state in all_states
    if verbose:
        print_path(all_paths, target_state, room_depth)
        print(all_states[target_state])
    return all_states[target_state]

def solve1(data):
    pods = parse(data)
    return solve(pods, 2)

def insert_folded_rows(pods):
    new_pods = defaultdict(set)
    for pod, positions in pods.items():
        for x, y in positions:
            if y <= 1:
                new_pods[pod].add((x,y))
            else:
                assert y == 2
                new_pods[pod].add((x,4))
    # insert rows 2 and 3:
    #  #D#C#B#A#
    #  #D#B#A#C#
    new_pods['D'].add((2,2))
    new_pods['C'].add((4,2))
    new_pods['B'].add((6,2))
    new_pods['A'].add((8,2))

    new_pods['D'].add((2,3))
    new_pods['B'].add((4,3))
    new_pods['A'].add((6,3))
    new_pods['C'].add((8,3))

    #print_state(to_hashable_state(pods), 2)
    #print_state(to_hashable_state(new_pods), 4)
    return new_pods

def solve2(data):
    pods = parse(data)
    pods = insert_folded_rows(pods)
    return solve(pods, 4)

assert solve1(EXAMPLE) == 12521
print(solve1(PUZZLE_INPUT))
assert solve2(EXAMPLE) == 44169
print(solve2(PUZZLE_INPUT))
