EXAMPLE = '''
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
'''

def parse_row(line):
    record, counts = line.split(' ')
    counts = [int(x) for x in counts.split(',')]
    return record, counts

def parse(data):
    return [parse_row(line) for line in data.strip().split('\n')]

def simplify_record(record):
    return '.'.join(x for x in record.split('.') if x)

assert simplify_record('????.#...#...') == '????.#.#'

def generate_all(record):
    index = record.find('?')
    if index < 0:
        yield record
    else:
        for r in '.#':
            replaced = record[:index] + r + record[index+1:]
            for x in generate_all(replaced):
                yield x

assert list(generate_all('.#')) == ['.#']
assert list(generate_all('?')) == ['.', '#']
assert list(generate_all('?.?')) == ['...', '..#', '#..', '#.#']

def count_springs(record):
    assert '?' not in record
    return [len(x) for x in record.split('.') if x]

assert count_springs('.#..#...###.') == [1,1,3]

def count_matching_combinations(record, counts):
    r = sum(1 for r in generate_all(record) if count_springs(r) == counts)
    #print(r)
    return r

assert count_matching_combinations('???.###', [1,1,3]) == 1
assert count_matching_combinations('.??..??...?##.', [1,1,3]) == 4

def solve1(data):
    rows = parse(data)
    return sum(count_matching_combinations(r, c) for r, c in rows)

assert solve1(EXAMPLE) == 21

with open('input') as f:
    data = f.read()

print(solve1(data))
