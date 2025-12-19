from itertools import combinations

EXAMPLE = '''
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
'''

def parse(s):
    def parse_lights(lights):
        assert lights.startswith('[') and lights.endswith(']')
        return [c == '#' for c in lights[1:-1]]

    def parse_button(button):
        assert button.startswith('(') and button.endswith(')')
        return {int(x) for x in button[1:-1].split(',')}

    def parse_joltages(joltages):
        assert joltages.startswith('{') and joltages.endswith('}')
        return [int(x) for x in joltages[1:-1].split(',')]

    def parse_line(line):
        parts = line.split()
        lights = parse_lights(parts[0])
        buttons = [parse_button(x) for x in parts[1:-1]]
        joltages = parse_joltages(parts[-1])
        return lights, buttons, joltages
    
    return [parse_line(line) for line in s.strip().split('\n')]

def press_buttons(lights, buttons):
    r = [False for _ in lights]
    for b in buttons:
        for i in b:
            r[i] = not r[i]
    #return {i for i, on in enumerate(r) if on}
    return r

def fewest_button_presses(lights, buttons):
    for i in range(1, len(buttons) + 1):
        for button_subset in combinations(buttons, i):
            if press_buttons(lights, button_subset) == lights:
                return i
    assert False

def solve1(s):
    puzzles = parse(s)
    result = 0
    for lights, buttons, _ in puzzles:
        result += fewest_button_presses(lights, buttons)
    return result

assert solve1(EXAMPLE) == 7

def lowest_nonzero(joltages):
    return min(x for x in joltages if x != 0)

def subtract_button_presses(joltages, button, button_press_count):
    if button_press_count == 0:
        return joltages
    else:
        return [
            joltage - button_press_count if index in button else joltage
            for index, joltage in enumerate(joltages)]

def remove_zero_indexes(joltages, buttons):
    zero_indexes = [i for i, n in enumerate(joltages) if n == 0]
    return [b for b in buttons if not any(i in b for i in zero_indexes)]

def fewest_button_presses_for_joltages(joltages, buttons):
    #print(joltages, buttons)
    if sum(joltages) == 0:
        assert all(x == 0 for x in joltages)
        return 0
    buttons = remove_zero_indexes(joltages, buttons)
    if len(buttons) == 0:
        #print(joltages)
        return None
    lowest_remaining = min(x for x in joltages if x != 0)
    assert lowest_remaining > 0
    # Pick an index with the fewest amount of matching buttons
    index = min(
        [index for index, n in enumerate(joltages) if n == lowest_remaining],
        key=lambda i: len([b for b in buttons if i in b]))
    #index = joltages.index(lowest_remaining)
    button_candidates = [b for b in buttons if index in b]
    #print(index, button_candidates)
    if len(button_candidates) == 0:
        # no solution possible with current buttons
        #print("X", joltages, buttons)
        return None
    first_candidate = button_candidates[0]
    if len(button_candidates) == 1:
        r = fewest_button_presses_for_joltages(
            subtract_button_presses(joltages, first_candidate, lowest_remaining),
            buttons)
        best = None if r is None else r + lowest_remaining
        #print("A", joltages, buttons, best)
        return best
    best = None
    remaining_buttons = [b for b in buttons if b != first_candidate]
    for button_presses in range(lowest_remaining + 1):
        r = fewest_button_presses_for_joltages(
            subtract_button_presses(joltages, first_candidate, button_presses),
            remaining_buttons
        )
        if r is None:
            continue
        r = r + button_presses
        if best is None or r < best:
            #print("New best", r)
            best = r
    #print("B", joltages, buttons, best)
    return best

def solve2(s):
    puzzles = parse(s)
    result = 0
    for _, buttons, joltages in puzzles:
        #print(buttons, joltages, "...")
        r = fewest_button_presses_for_joltages(joltages, buttons)
        #print(buttons, joltages, r)
        assert r is not None and r > 0
        result += r
    return result

assert solve2(EXAMPLE) == 33

with open('input') as f:
    s = f.read()

print(solve1(s))
print(solve2(s))
