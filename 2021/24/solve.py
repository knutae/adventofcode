def parse(data):
    lines = data.strip().split('\n')
    return [line.split() for line in lines]

def run_block(instructions, input_number, input_index, env):
    for instruction in instructions:
        op, var, *rest = instruction
        if op == 'inp':
            assert len(rest) == 0
            env[var] = int(input_number[input_index])
            input_index += 1
            continue
        assert len(rest) == 1
        arg = rest[0]
        if arg in 'wxyz':
            arg = env[arg]
        else:
            arg = int(arg)
        if op == 'add':
            env[var] += arg
        elif op == 'mul':
            env[var] *= arg
        elif op == 'div':
            env[var] //= arg
        elif op == 'mod':
            env[var] %= arg
        elif op == 'eql':
            env[var] = 1 if arg == env[var] else 0
        else:
            assert False, op
    return input_index

def run(instructions, input_number):
    env = {'w':0, 'x':0, 'y':0, 'z':0}
    final_input_index = run_block(instructions, input_number, 0, env)
    assert final_input_index == len(input_number)
    return env['z']

def split_instructions(instructions):
    blocks = []
    current_block = None
    for instruction in instructions:
        #print(instruction)
        if instruction[0] == 'inp':
            if current_block:
                blocks.append(current_block)
            current_block = []
        current_block.append(instruction)
    assert current_block
    blocks.append(current_block)
    return blocks

def filter_block(block, op, var):
    prefix = [op, var]
    return [x for x in block if x[:2] == prefix]

def solve_block(block, target_z, w_range):
    # HACKISH: should find a way to narrow the search range
    last_y = int(filter_block(block, 'add', 'y')[-1][-1])
    second_x = int(filter_block(block, 'add', 'x')[1][-1])
    leniency = max(abs(last_y), abs(second_x))
    z_range = set()
    for base_z in (target_z // 26, target_z, target_z * 26):
        z_range |= set(range(base_z - 26 - leniency, base_z + 35 + leniency))
    for w in w_range:
        for z in z_range:
            env = {'x':0, 'y':0, 'z':z, 'w':0}
            run_block(block, str(w), 0, env)
            if env['z'] == target_z:
                yield w, z


def solve1(instructions):
    blocks = split_instructions(instructions)
    targets = {0: 0}
    ten_multiplier = 1
    w_range = range(1,10)
    for block in reversed(blocks):
        new_targets = {}
        for target_z, input_num in targets.items():
            for w, z in solve_block(block, target_z, w_range):
                new_targets[z] = max(new_targets.get(z, 0), w*ten_multiplier + input_num)
        ten_multiplier *= 10
        print(f'{len(targets)} -> {len(new_targets)}')
        targets = new_targets
    print(targets)
    result = max(targets.values())
    assert run(instructions, str(result)) == 0
    return result

def solve2(instructions):
    blocks = split_instructions(instructions)
    targets = {0: 0}
    ten_multiplier = 1
    w_range = range(1,10)
    for block in reversed(blocks):
        new_targets = {}
        for target_z, input_num in targets.items():
            for w, z in solve_block(block, target_z, w_range):
                if z in new_targets:
                    new_targets[z] = min(new_targets[z], w*ten_multiplier + input_num)
                else:
                    new_targets[z] = w*ten_multiplier + input_num
        ten_multiplier *= 10
        print(f'{len(targets)} -> {len(new_targets)}')
        targets = new_targets
    print(targets)
    result = max(targets.values())
    print(result, f'{result:014}')
    assert run(instructions, f'{result:014}') == 0
    return result

with open('input') as f:
    instructions = parse(f.read())

print(solve1(instructions))
print(solve2(instructions))
