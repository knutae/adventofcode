EXAMPLE = '''
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
'''

def parse_line(line, label, sep):
    first, rest = line.split(': ')
    assert first == label
    xc, yc = rest.split(', ')
    assert xc.startswith('X' + sep)
    assert yc.startswith('Y' + sep)
    assert len(sep) == 1
    x = int(xc[2:])
    y = int(yc[2:])
    return x, y

def parse_machine(section):
    [a, b, c] = section.split('\n')
    a = parse_line(a, 'Button A', '+')
    b = parse_line(b, 'Button B', '+')
    c = parse_line(c, 'Prize', '=')
    return a, b, c

def parse(data):
    sections = data.strip().split('\n\n')
    return [parse_machine(s) for s in sections]

def prize_cost(a, b, prize):
    xa, ya = a
    xb, yb = b
    xp, yp = prize
    solutions = []
    for a_count in range(101):
        x = xa * a_count
        y = ya * a_count
        if x > xp or y > yp:
            # one button too far
            break
        if (xp - x) % xb > 0 or (yp - y) % yb > 0:
            # modulo math prevents a solution
            continue
        b_count = (xp - x) // xb
        if b_count <= 100 and (yp - y) // yb == b_count:
            solutions.append((a_count, b_count))
    if not solutions:
        return 0 # to make summing easy
    return min(a_count * 3 + b_count for a_count, b_count in solutions)

def solve1(data):
    machines = parse(data)
    return sum(prize_cost(*machine) for machine in machines)

assert solve1(EXAMPLE) == 480    

with open('input') as f:
    data = f.read()

print(solve1(data))
