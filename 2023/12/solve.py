from functools import cache

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
    counts = tuple(int(x) for x in counts.split(','))
    return record, counts

def parse(data):
    return [parse_row(line) for line in data.strip().split('\n')]

def simplify_record(record):
    return '.'.join(x for x in record.split('.') if x)

assert simplify_record('????.#...#...') == '????.#.#'

def string_matches(record, s):
    return all(a == '?' or a == b for a,b in zip(record, s))

@cache
def count_matching_strings(record, counts):
    length = len(record)
    if len(counts) == 0:
        return 1
    first_count, *rest_counts = counts
    rest_counts = tuple(rest_counts)
    result = 0
    if len(rest_counts) == 0:
        for i in range(length - first_count + 1):
            s = '.' * i + '#' * first_count + '.' * (length - first_count - i)
            #assert len(s) == length
            if string_matches(record, s):
                result += 1
    else:
        partial = '#'*first_count + '.'
        min_rest_length = sum(rest_counts) + len(rest_counts) - 1
        for i in range(length - min_rest_length):
            prefix = '.' * i + partial
            if not string_matches(record, prefix):
                continue
            rest_record = record[len(prefix):]
            result += count_matching_strings(rest_record, rest_counts)
    return result

def solve1(data):
    rows = parse(data)
    return sum(count_matching_strings(r, c) for r, c in rows)

assert solve1(EXAMPLE) == 21

def unfold_row(row):
    record, counts = row
    return simplify_record('?'.join(record for _ in range(5))), tuple(counts * 5)

def solve2(data):
    rows = [unfold_row(row) for row in parse(data)]
    return sum(count_matching_strings(r, c) for r, c in rows)

assert solve2(EXAMPLE) == 525152

with open('input') as f:
    data = f.read()

print(solve1(data))
print(solve2(data))
