TEST_INPUT = '''
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
'''

def parse_group(input):
    pairs = dict()
    for kv in input.split():
        assert ':' in kv
        [k, v] = kv.split(':')
        pairs[k] = v
    return pairs

def parse(input):
    return [parse_group(x) for x in input.strip().split('\n\n')]

def solve1(passports):
    required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'} # not cid
    valid = 0
    for passport in passports:
        if all(k in passport for k in required):
            valid += 1
    return valid

passports = parse(TEST_INPUT)
assert solve1(passports) == 2
with open('input') as f:
    passports = parse(f.read())
print(solve1(passports))
