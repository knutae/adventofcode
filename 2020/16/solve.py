EXAMPLE = '''
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
'''

def parse_range(rangespec):
    [a, b] = rangespec.split('-')
    return range(int(a), int(b)+1)

def parse_field(line):
    [name, rest] = line.split(': ')
    ranges = [parse_range(r) for r in rest.split(' or ')]
    return name, ranges

def parse_ticket(line):
    return [int(x) for x in line.split(',')]

def parse(input):
    [fields, your_ticket, nearby_tickets] = input.strip().split('\n\n')
    fields = dict(parse_field(line) for line in fields.split('\n'))
    your_ticket = your_ticket.split('\n')
    assert len(your_ticket) == 2 and your_ticket[0] == 'your ticket:'
    your_ticket = parse_ticket(your_ticket[1])
    nearby_tickets = nearby_tickets.split('\n')
    assert nearby_tickets[0] == 'nearby tickets:'
    nearby_tickets = [parse_ticket(line) for line in nearby_tickets[1:]]
    return fields, your_ticket, nearby_tickets

def valid_field_value(n, ranges):
    return any(n in r for r in ranges)

def valid_for_any_field(n, fields):
    return any(valid_field_value(n, ranges) for ranges in fields.values())

def solve1(input):
    fields, your_ticket, nearby_tickets = parse(input)
    invalid = []
    for ticket in nearby_tickets:
        for n in ticket:
            if not valid_for_any_field(n, fields):
                invalid.append(n)
    #print(invalid)
    return sum(invalid)

assert solve1(EXAMPLE) == 71

def detect_field_order(fields, your_ticket, nearby_tickets):
    valid_tickets = [ticket for ticket in nearby_tickets if all(valid_for_any_field(n, fields) for n in ticket)]
    index_candidates = [
        {field for field in fields if all(valid_field_value(ticket[i], fields[field]) for ticket in valid_tickets)}
        for i in range(len(fields))
    ]
    #print(index_candidates)
    while any(len(c) > 1 for c in index_candidates):
        for c in index_candidates:
            if len(c) == 1:
                c = next(iter(c))
                for d in index_candidates:
                    if len(d) > 1 and c in d:
                        d.remove(c)
    #print(index_candidates)
    return [next(iter(c)) for c in index_candidates]

assert detect_field_order(*parse(EXAMPLE)) == ['row', 'class', 'seat']

def solve2(input):
    fields, your_ticket, nearby_tickets = parse(input)
    field_order = detect_field_order(fields, your_ticket, nearby_tickets)
    #print(field_order)
    mult = 1
    for i, field in enumerate(field_order):
        if field.startswith('departure'):
            value = your_ticket[i]
            print(f'{field}: {value}')
            mult *= value
    return mult

with open('input') as f:
    input = f.read()

print(solve1(input))
print(solve2(input))
