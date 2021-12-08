EXAMPLE = '''
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
'''

def parse_line(line):
    return [[set(x) for x in part.split()] for part in line.split(' | ')]

def parse(data):
    return [parse_line(line) for line in data.strip().split('\n')]

#print(parse(EXAMPLE))

def solve1(lines):
    count = 0
    for signal_patterns, output_values in lines:
        assert len(signal_patterns) == 10
        count += len([x for x in output_values if len(x) in (2, 4, 3, 7)])
    return count

assert solve1(parse(EXAMPLE)) == 26

def solve_line(signal_patterns, output_values):
    def unique_pattern(predicate):
        matches = [p for p in signal_patterns if predicate(p)]
        assert len(matches) == 1, matches
        return set(matches[0])

    def pattern_with_length(n):
        return unique_pattern(lambda p: len(p) == n)

    # unique lengths
    one = pattern_with_length(2)
    four = pattern_with_length(4)
    seven = pattern_with_length(3)
    eight = pattern_with_length(7)
    # length 6
    six = unique_pattern(lambda p: len(p) == 6 and len(p & one) == 1)
    nine = unique_pattern(lambda p: len(p) == 6 and p > four)
    zero = unique_pattern(lambda p: len(p) == 6 and p != six and p != nine)
    # length 5
    three = unique_pattern(lambda p: len(p) == 5 and p > one)
    five = unique_pattern(lambda p: len(p) == 5 and p != three and p < nine)
    two = unique_pattern(lambda p: len(p) == 5 and p != three and p != five)
    table = [zero, one, two, three, four, five, six, seven, eight, nine]
    output_str = ''.join(str(table.index(v)) for v in output_values)
    return int(output_str)

def solve2(lines):
    return sum(solve_line(signal_patterns, output_values) for signal_patterns, output_values in lines)

assert solve_line(*parse_line('acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf')) == 5353
assert solve2(parse(EXAMPLE)) == 61229

with open('input') as f:
    lines = parse(f.read())

print(solve1(lines))
print(solve2(lines))
