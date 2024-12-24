SMALL_EXAMPLE = '''
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
'''

EXAMPLE = '''
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
'''

def parse_initial(line):
    wire, value = line.split(': ')
    return wire, int(value)

def parse_gate(line):
    lhs, rhs = line.split(' -> ')
    v1, op, v2 = lhs.split(' ')
    return rhs, (op, v1, v2)

def parse(data):
    initial, gates = data.strip().split('\n\n')
    initial = dict(parse_initial(line) for line in initial.split('\n'))
    gates = dict(parse_gate(line) for line in gates.split('\n'))
    return initial, gates

def force_value(values, gates, value):
    if value in values:
        return values[value]
    assert value in gates
    op, a, b = gates[value]
    a_value = force_value(values, gates, a)
    b_value = force_value(values, gates, b)
    if op == 'AND':
        v = a_value & b_value
    elif op == 'OR':
        v = a_value | b_value
    elif op == 'XOR':
        v = a_value ^ b_value
    else:
        assert False
    values[value] = v
    return v

def solve1(data):
    values, gates = parse(data)
    z_values = list(sorted(v for v in gates if v.startswith('z')))
    result = [force_value(values, gates, z) for z in z_values]
    result = ''.join(str(x) for x in reversed(result))
    return int(result, 2)

assert solve1(SMALL_EXAMPLE) == 4
assert solve1(EXAMPLE) == 2024

with open('input') as f:
    data = f.read()

print(solve1(data))
