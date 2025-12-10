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


with open('input') as f:
    s = f.read()

print(solve1(s))
